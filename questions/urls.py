from django.urls import path
from .views import ConceptListAPIView

urlpatterns = [
    path(
        "<int:document_id>/concepts/",
        ConceptListAPIView.as_view()
    ),
]
