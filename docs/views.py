from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from .serializers import DocumentSerializer
from rest_framework.parsers import (
    MultiPartParser,
    FormParser
)


from docs.models import Document, Status

from docs.tasks import process_document


class DocumentUploadAPIView(APIView):

    permission_classes = [
    ]


    parser_classes = [
        MultiPartParser,
        FormParser
    ]



    def post(self, request):
        print("USER:", request.user)
        print("AUTH:", request.auth)
        print("HEADER:", request.headers.get("Authorization"))

        file = request.FILES["file"]


        document = Document.objects.create(

            owner=request.user,

            file=file,

            title=file.name,

            status=Status.PROCESSING

        )


        process_document.delay(
            document.id
        )


        return Response(
            {
                "message":
                "Document uploaded. Processing started",

                "document_id":
                document.id
            }
        )
        
from docs.tasks import extract_concepts_task



class GenerateMindMapAPIView(APIView):

    permission_classes=[
        IsAuthenticated
    ]


    def post(self, request, id):


        document = Document.objects.get(
            id=id,
            owner=request.user
        )


        extract_concepts_task.delay(
            document.id
        )


        return Response(
            {
                "message":
                "Mind map generation started"
            }
        )
class DocumentListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        documents = Document.objects.filter(
            owner=request.user
        ).order_by("-created_at")

        serializer = DocumentSerializer(
            documents,
            many=True
        )

        return Response(serializer.data)

