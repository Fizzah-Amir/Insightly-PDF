from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from itertools import groupby

from docs.models import Document, Status
from .models import Concept


@login_required
def concepts_view(request, document_id):
    document = get_object_or_404(Document, id=document_id, owner=request.user)

    grouped = []
    if document.status == Status.COMPLETED:
        concepts = Concept.objects.filter(document=document).order_by("page_number")
        for page_number, items in groupby(concepts, key=lambda c: c.page_number):
            grouped.append({
                "page_number": page_number,
                "concepts": list(items),
            })

    return render(request, "questions/concepts.html", {
        "document": document,
        "grouped": grouped,
        "active_nav": "documents",
    })