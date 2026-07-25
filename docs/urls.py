from django.urls import path
from .views import (
    DocumentUploadAPIView,
    DocumentAskAPIView,
    DocumentListAPIView,
    DocumentDetailAPIView,
    DocumentDeleteAPIView,
    DocumentCompareAPIView
)

urlpatterns = [

    path(
        "upload/",
        DocumentUploadAPIView.as_view()
    ),
    path(
        "compare/",
        DocumentCompareAPIView.as_view()
    ),
    path(
    "<int:document_id>/ask/",
    DocumentAskAPIView.as_view()
    ),
    path(
    "<int:document_id>/",
    DocumentDetailAPIView.as_view()
),
    path(
        "",
        DocumentListAPIView.as_view()
    ),
    path(
    "<int:document_id>/delete/",
    DocumentDeleteAPIView.as_view()
),
]