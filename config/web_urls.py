from django.urls import path
from docs.web_views import (
    document_list,
    document_upload,
    document_detail,
    document_delete,
    compare_view,
)
from questions.web_views import concepts_view

urlpatterns = [
    path("documents/", document_list, name="web_document_list"),
    path("documents/upload/", document_upload, name="web_document_upload"),
    path("documents/<int:document_id>/", document_detail, name="web_document_detail"),
    path("documents/<int:document_id>/delete/", document_delete, name="web_document_delete"),
    path("documents/<int:document_id>/concepts/", concepts_view, name="web_concepts"),
    path("compare/", compare_view, name="web_compare"),
]
