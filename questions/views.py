from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from docs.models import Document
from .models import Concept
from .serializers import ConceptSerializer


class ConceptListAPIView(APIView):
    """
    Returns extracted concepts for a document, grouped implicitly by
    page_number (frontend can group them). Only the document owner
    can see them.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, document_id):

        try:
            document = Document.objects.get(
                id=document_id,
                owner=request.user
            )
        except Document.DoesNotExist:
            return Response(
                {"error": "Document not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if document.status != "completed":
            return Response(
                {
                    "error": "Document is still processing. Concepts aren't ready yet.",
                    "status": document.status
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        concepts = Concept.objects.filter(
            document=document
        ).order_by("page_number")

        serializer = ConceptSerializer(concepts, many=True)

        return Response(serializer.data)