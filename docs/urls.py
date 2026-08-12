from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views import (
    DocumentUploadAPIView,
    GenerateMindMapAPIView,
    DocumentListAPIView,
)
from .chat_views import (
    CreateConversationAPIView,
    ChatHistoryAPIView,
    ChatMessageAPIView
)

urlpatterns = [
     path(
        "api/token/",
        TokenObtainPairView.as_view()
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view()
    ),
 path(
        "",
        DocumentListAPIView.as_view()
    ),

path(
    "upload/",
    DocumentUploadAPIView.as_view()
),


path(
    "<int:id>/mindmap/",
    GenerateMindMapAPIView.as_view()
),

path(
    "chat/message/",
    ChatMessageAPIView.as_view()
),
path(
        "chat/start/",
        CreateConversationAPIView.as_view()
    ),

    path(
        "chat/history/<int:document_id>/",
        ChatHistoryAPIView.as_view()
    ),

]