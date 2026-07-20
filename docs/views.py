from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .tasks import process_document
from .models import Document, Status
from .serializers import DocumentSerializer
from ai_engine.services import (
    extract_pdf_text,
    split_documents,
    generate_embeddings,
    search_similar_chunks,
    generate_answer,
)

from ai_engine.models import DocumentChunk


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

            pdf_path = document.file.path

            try:
                documents = extract_pdf_text(pdf_path)

                chunks = split_documents(documents)

                embeddings = generate_embeddings(chunks)

                for chunk, embedding in zip(chunks, embeddings):
                    DocumentChunk.objects.create(
                        document=document,
                        content=chunk.page_content,
                        embedding=embedding
                    )

                document.status = Status.COMPLETED
                document.save()

                return Response({
                    "message": "PDF uploaded and processed successfully",
                    "document_id": document.id,
                    "chunks_created": len(chunks)
                })

            except Exception as e:

                document.status = Status.FAILED
                document.save()

                return Response(
                    {
                        "error": "PDF processing failed",
                        "details": str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
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

        answer = generate_answer(
            question,
            chunks
        )

        return Response({
            "question": question,
            "answer": answer
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