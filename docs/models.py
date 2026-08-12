from django.db import models
from django.conf import settings


class Status(models.TextChoices):
    PROCESSING = "PROCESSING"
    READY = "READY"
    FAILED = "FAILED"


class MindMapStatus(models.TextChoices):
    NOT_STARTED = "NOT_STARTED"
    PROCESSING = "PROCESSING"
    READY = "READY"
    FAILED = "FAILED"



class Document(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    file = models.FileField(
        upload_to="documents/"
    )

    title = models.CharField(
        max_length=255
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PROCESSING
    )

    mindmap_status = models.CharField(
        max_length=20,
        choices=MindMapStatus.choices,
        default=MindMapStatus.NOT_STARTED
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


class Conversation(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="conversations"
    )

    title = models.CharField(
        max_length=255,
        default="New Chat"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title

class ChatMessage(models.Model):

    ROLE_CHOICES = (
        ("user", "User"),
        ("assistant", "Assistant"),
    )

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    content = models.TextField()

    citations = models.JSONField(
        default=list,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["created_at"]


    def __str__(self):
        return f"{self.role}: {self.content[:40]}"