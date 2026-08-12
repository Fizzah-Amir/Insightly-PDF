from django.db import models
from docs.models import Document


class Concept(models.Model):

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="concepts"
    )

    name = models.CharField(max_length=255)

    page_number = models.IntegerField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("document", "name", "page_number")

    def __str__(self):
        return f"{self.name} (p.{self.page_number})"


class ConceptRelationship(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="relationships")
    from_concept = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name="outgoing")
    to_concept = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name="incoming")
    relationship = models.CharField(max_length=100)

    class Meta:
        unique_together = ("document", "from_concept", "to_concept")