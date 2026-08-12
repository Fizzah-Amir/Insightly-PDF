from celery import shared_task

from docs.models import Document, MindMapStatus

from ai_engine.services import (
    extract_concepts_for_document,
    extract_concept_relationships
)

from .models import Concept, ConceptRelationship



@shared_task
def extract_concepts_task(document_id):

    document = Document.objects.get(
        id=document_id
    )

    try:

        document.mindmap_status = (
            MindMapStatus.PROCESSING
        )
        document.save()


        concepts = extract_concepts_for_document(
            document
        )


        for item in concepts:

            Concept.objects.get_or_create(

                document=document,

                name=item["name"],

                page_number=item["page_number"]

            )


        # after concepts are created
        generate_relationships_task.delay(
            document_id
        )


    except Exception as e:


        document.mindmap_status = (
            MindMapStatus.FAILED
        )

        document.save()


        raise e





@shared_task
def generate_relationships_task(document_id):
    document = Document.objects.get(id=document_id)
    concepts = Concept.objects.filter(document=document)
    concept_names = list(concepts.values_list("name", flat=True).distinct())
    name_to_concept = {c.name: c for c in concepts}

    edges = extract_concept_relationships(concept_names)
    for edge in edges:
        from_name = edge.get("from")
        to_name = edge.get("to")
        rel = edge.get("relationship", "related to")
        from_c = name_to_concept.get(from_name)
        to_c = name_to_concept.get(to_name)
        if from_c and to_c:
            ConceptRelationship.objects.get_or_create(
                document=document,
                from_concept=from_c,
                to_concept=to_c,
                defaults={"relationship": rel},
            )
    document.mindmap_status = MindMapStatus.READY
    document.save()