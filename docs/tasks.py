import time

from celery import shared_task
from questions.tasks import extract_concepts_task
from docs.models import Document, Status
from ai_engine.models import DocumentChunk

from ai_engine.services import (
    extract_pdf_text,
    split_documents,
    generate_embeddings,
    extract_concepts_for_document,
    extract_concept_relationships,
)

from questions.models import (
    Concept,
    ConceptRelationship
)


@shared_task
def process_document(document_id):

    try:

        document = Document.objects.get(
            id=document_id
        )

        start_time = time.time()


        # -------------------------
        # PDF Extraction
        # -------------------------

        t = time.time()

        pdf_documents = extract_pdf_text(
            document.file.path
        )

        print(
            "PDF extraction:",
            time.time() - t
        )


        # -------------------------
        # Chunking
        # -------------------------

        t = time.time()

        chunks = split_documents(
            pdf_documents
        )

        print(
            "Chunking:",
            time.time() - t
        )


        # -------------------------
        # Embeddings
        # -------------------------

        t = time.time()

        embeddings = generate_embeddings(
            chunks
        )

        print(
            "Embedding:",
            time.time() - t
        )


        # -------------------------
        # Save Chunks
        # -------------------------

        t = time.time()

        chunk_objects = []

        for chunk, embedding in zip(
            chunks,
            embeddings
        ):

            clean_content = (
                chunk.page_content
                .replace("\x00", "")
                .strip()
            )

            chunk_objects.append(
                DocumentChunk(
                    document=document,
                    content=clean_content,
                    page_number=chunk.metadata.get("page"),
                    embedding=embedding
                )
            )


        DocumentChunk.objects.bulk_create(
            chunk_objects,
            batch_size=500
        )


        print(
            "Database insert:",
            time.time() - t
        )


        # -------------------------
        # Document Ready
        # -------------------------

        document.status = Status.READY
        document.save()


        extract_concepts_task.delay(
         document.id
                    )


        print(
            "TOTAL PROCESSING TIME:",
            time.time() - start_time
        )


        # -------------------------
        # Start Concept Extraction
        # -------------------------

        extract_concepts_task.delay(
            document.id
        )


    except Document.DoesNotExist:

        print(
            f"Document {document_id} does not exist"
        )

        return


    except Exception as e:

        print(
            "PROCESS DOCUMENT FAILED:",
            str(e)
        )


        try:
            document.status = Status.FAILED
            document.save()

        except Exception:
            pass

        raise e



# ==================================================
# Concept / Mind Map Extraction
# ==================================================

@shared_task
def extract_concepts_task(document_id):

    try:

        document = Document.objects.get(
            id=document_id
        )


        document.mindmap_status = "PROCESSING"
        document.save()



        # -------------------------
        # Extract Concepts using LLM
        # -------------------------

        concepts = extract_concepts_for_document(
            document
        )


        concept_objects = []


        for item in concepts:

            concept_objects.append(
                Concept(
                    document=document,
                    name=item["name"],
                    page_number=item["page_number"]
                )
            )


        Concept.objects.bulk_create(
            concept_objects,
            ignore_conflicts=True
        )



        # -------------------------
        # Generate Relationships
        # -------------------------

        names = list(
            Concept.objects.filter(
                document=document
            )
            .values_list(
                "name",
                flat=True
            )
        )


        edges = extract_concept_relationships(
            names
        )
        print("EDGES RETURNED:", edges)
        print("NUMBER OF CONCEPTS:", len(names))

        # -------------------------
        # Build name -> Concept lookup
        # -------------------------

        concept_lookup = {
            c.name: c
            for c in Concept.objects.filter(document=document)
        }

        relationship_objects = []

        for edge in edges:

            from_c = concept_lookup.get(edge["from"])
            to_c = concept_lookup.get(edge["to"])

            if from_c and to_c:
                relationship_objects.append(
                    ConceptRelationship(
                        document=document,
                        from_concept=from_c,
                        to_concept=to_c,
                        relationship=edge["relationship"]
                    )
                )


        ConceptRelationship.objects.bulk_create(
            relationship_objects,
            ignore_conflicts=True
        )



        # -------------------------
        # Finished
        # -------------------------

        document.mindmap_status = "READY"
        document.save()


        print(
            "Concept extraction completed"
        )


    except Document.DoesNotExist:

        print(
            f"Document {document_id} does not exist"
        )

        return



    except Exception as e:


        print(
            "MIND MAP FAILED:",
            str(e)
        )


        try:

            document.mindmap_status = "FAILED"
            document.save()

        except Exception:
            pass


        raise e