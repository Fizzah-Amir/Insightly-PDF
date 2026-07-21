from celery import shared_task

from docs.models import Document, Status

from ai_engine.services import (
    extract_pdf_text,
    split_documents,
    generate_embeddings,
)

from ai_engine.models import DocumentChunk


@shared_task
def process_document(document_id):

    document = Document.objects.get(
        id=document_id
    )

    try:

        pdf_path = document.file.path

        documents = extract_pdf_text(pdf_path)

        chunks = split_documents(documents)

        embeddings = generate_embeddings(chunks)


        for chunk, embedding in zip(chunks, embeddings):

            DocumentChunk.objects.create(
                document=document,
                content=chunk.page_content,
                embedding=embedding
            )


        document.status = Status.COMPLETED
        document.save()


    except Exception as e:

        document.status = Status.FAILED
        document.save()

        raise e