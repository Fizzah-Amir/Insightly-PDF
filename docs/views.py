from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .tasks import process_document
from .models import Document, Status
from .serializers import DocumentSerializer
from .tasks import process_document
from rest_framework.generics import RetrieveAPIView
from ai_engine.models import DocumentChunk
from ai_engine.services import (
    extract_pdf_text,
    split_documents,
    generate_embeddings,
    search_similar_chunks,
    generate_answer,
    compare_documents,
)
class DocumentUploadAPIView(APIView):

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


    def post(self, request):

        serializer = DocumentSerializer(data=request.data)

        if serializer.is_valid():

            document = serializer.save(
                owner=request.user,
                status=Status.PROCESSING
            )


            # Background task start
            process_document.delay(document.id)


            return Response(
                {
                    "message": "PDF uploaded. Processing started.",
                    "document_id": document.id,
                    "status": "processing"
                },
                status=status.HTTP_201_CREATED
            )


        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
class DocumentAskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, document_id):

        question = request.data.get("question")

        chunks = search_similar_chunks(
            question,
            document_id
        )

        result = generate_answer(
            question,
            chunks
        )

        return Response({
            "question": question,
            "answer": result["answer"],
            "sources": result["sources"]
        })
class DocumentListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        documents = Document.objects.filter(
            owner=request.user
        )

        serializer = DocumentSerializer(
            documents,
            many=True
        )

        return Response(serializer.data)
class DocumentDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, document_id):

        try:
            document = Document.objects.get(
                id=document_id,
                owner=request.user
            )

        except Document.DoesNotExist:
            return Response(
                {
                    "error": "Document not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )


        document.delete()

        return Response(
            {
                "message": "Document deleted successfully"
            },
            status=status.HTTP_204_NO_CONTENT
        )
class DocumentDetailAPIView(RetrieveAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
class DocumentCompareAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        question = request.data.get("question")
        document_ids = request.data.get("document_ids")

        if not question:
            return Response(
                {"error": "question is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not document_ids or not isinstance(document_ids, list) or len(document_ids) < 2:
            return Response(
                {"error": "document_ids must be a list of at least 2 document ids"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ownership check: only compare documents the user actually owns,
        # and only ones that finished processing.
        owned_documents = Document.objects.filter(
            id__in=document_ids,
            owner=request.user,
            status=Status.COMPLETED
        )

        owned_ids = list(owned_documents.values_list("id", flat=True))

        missing_ids = set(document_ids) - set(owned_ids)
        if missing_ids:
            return Response(
                {
                    "error": "Some documents were not found, not yours, or still processing.",
                    "invalid_ids": list(missing_ids)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        result = compare_documents(question, owned_ids)

        return Response({
            "question": question,
            "document_ids": owned_ids,
            "agreements": result["agreements"],
            "contradictions": result["contradictions"],
            "unique_points": result["unique_points"],
        })