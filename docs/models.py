from django.db import models
from django.conf import settings

class Status(models.TextChoices):
    UPLOADED = "uploaded", "Uploaded"
    PROCESSING = "processing", "Processing"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"
    
class Document(models.Model):

    title = models.CharField(max_length=255)

    file = models.FileField(
        upload_to="documents/"
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    status = models.CharField(
    max_length=20,
    choices=Status.choices,
    default=Status.UPLOADED,
    )

    def __str__(self):
        return self.title