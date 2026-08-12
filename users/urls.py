from django.urls import path
from .views import LoginAPIView, SignupAPIView

urlpatterns = [
    path("login/", LoginAPIView.as_view()),
    path("signup/", SignupAPIView.as_view()),
]