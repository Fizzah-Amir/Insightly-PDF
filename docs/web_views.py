from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Document, Status
from .tasks import process_document
from ai_engine.services import search_similar_chunks, generate_answer, compare_documents


@login_required
def document_list(request):
    documents = Document.objects.filter(
        owner=request.user
    ).order_by("-uploaded_at")

    return render(request, "docs/document_list.html", {
        "documents": documents,
        "active_nav": "documents",
    })


@login_required
def document_upload(request):
    if request.method == "POST":
        title = request.POST.get("title")
        file = request.FILES.get("file")

        if not title or not file:
            messages.error(request, "Please provide both a title and a PDF file.")
            return render(request, "docs/document_upload.html", {"active_nav": "upload"})

        document = Document.objects.create(
            title=title,
            file=file,
            owner=request.user,
            status=Status.PROCESSING,
        )

        process_document.delay(document.id)

        messages.success(request, f'"{title}" uploaded. Processing has started.')
        return redirect("web_document_list")

    return render(request, "docs/document_upload.html", {"active_nav": "upload"})


@login_required
def document_detail(request, document_id):
    document = get_object_or_404(Document, id=document_id, owner=request.user)

    answer = None
    sources = None
    question = None

    if request.method == "POST":
        question = request.POST.get("question")

        if document.status != Status.COMPLETED:
            messages.error(request, "This document is still processing — try again shortly.")
        elif question:
            chunks = search_similar_chunks(question, document.id)
            result = generate_answer(question, chunks)
            answer = result["answer"]
            sources = result["sources"]

    return render(request, "docs/document_detail.html", {
        "document": document,
        "question": question,
        "answer": answer,
        "sources": sources,
        "active_nav": "documents",
    })


@login_required
def document_delete(request, document_id):
    document = get_object_or_404(Document, id=document_id, owner=request.user)

    if request.method == "POST":
        title = document.title
        document.delete()
        messages.success(request, f'"{title}" was deleted.')

    return redirect("web_document_list")


@login_required
def compare_view(request):
    documents = Document.objects.filter(
        owner=request.user,
        status=Status.COMPLETED
    ).order_by("-uploaded_at")

    result = None
    question = None
    selected_ids = []

    if request.method == "POST":
        question = request.POST.get("question")
        selected_ids = request.POST.getlist("document_ids")

        if not question or len(selected_ids) < 2:
            messages.error(request, "Pick at least 2 documents and enter a question.")
        else:
            owned_ids = list(
                documents.filter(id__in=selected_ids).values_list("id", flat=True)
            )
            result = compare_documents(question, owned_ids)
            selected_ids = [str(i) for i in owned_ids]

    return render(request, "docs/compare.html", {
        "documents": documents,
        "result": result,
        "question": question,
        "selected_ids": selected_ids,
        "active_nav": "compare",
    })