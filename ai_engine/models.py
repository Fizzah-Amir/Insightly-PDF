from django.db import models
from docs.models import Document
from pgvector.django import VectorField


class DocumentChunk(models.Model):

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="chunks"
    )

    content = models.TextField()

    embedding = VectorField(
        dimensions=384,
        null=True,
        blank=True
    )


def save_chunks_with_embeddings(chunks, embeddings, document):

    for chunk, embedding in zip(chunks, embeddings):

        DocumentChunk.objects.create(
            document=document,
            content=chunk.page_content,
            embedding=embedding
        )