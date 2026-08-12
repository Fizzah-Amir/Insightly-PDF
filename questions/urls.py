from .views import MindMapAPIView
from django.urls import path, include

urlpatterns=[

path(
"mindmap/<int:document_id>/",
MindMapAPIView.as_view()
)

]