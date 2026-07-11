from django.db import models
from django.conf import settings
# Create your models here.

class Document(models.Model):
    class Status(models.TextChoices):
        UPLOADED = "uploaded", "Uploaded"
        PROCESSING = "processing", "Processing"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"
    owner=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="documents"
    )
    title=models.CharField(max_length=255)
    file=models.FileField(upload_to="documents/")
    status=models.CharField(max_length=20,
                            choices=Status.choices,
                            default=Status.UPLOADED)
    uploaded_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title