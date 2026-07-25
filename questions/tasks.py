from celery import shared_task

from docs.models import Document
from ai_engine.services import extract_concepts_for_document
from .models import Concept


@shared_task
def extract_concepts_task(document_id):

    document = Document.objects.get(id=document_id)

    concepts = extract_concepts_for_document(document)

    for item in concepts:
        Concept.objects.get_or_create(
            document=document,
            name=item["name"],
            page_number=item["page_number"],
        )