from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from itertools import groupby
import json

from docs.models import Document, Status
from .models import Concept, ConceptRelationship


@login_required
def concepts_view(request, document_id):
    document = get_object_or_404(Document, id=document_id, owner=request.user)

    grouped = []
    nodes = []
    edges = []

    if document.status == Status.READY:
        concepts = Concept.objects.filter(document=document).order_by("page_number")
        for page_number, items in groupby(concepts, key=lambda c: c.page_number):
            grouped.append({
                "page_number": page_number,
                "concepts": list(items),
            })

        seen_names = set()
        for c in concepts:
            if c.name not in seen_names:
                nodes.append({"id": c.name, "label": c.name})
                seen_names.add(c.name)

        relationships = ConceptRelationship.objects.filter(document=document)
        for r in relationships:
            edges.append({
                "from": r.from_concept,
                "to": r.to_concept,
                "label": r.relationship,
            })

    return render(request, "questions/concepts.html", {
        "document": document,
        "grouped": grouped,
        "mindmap_nodes": json.dumps(nodes),
        "mindmap_edges": json.dumps(edges),
        "active_nav": "documents",
    })