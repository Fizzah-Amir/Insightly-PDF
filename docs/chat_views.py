from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import (
    Document,
    Conversation,
    ChatMessage
)

from .serializers import ConversationSerializer

from ai_engine.services import (
    search_similar_chunks,
    generate_answer
)


class CreateConversationAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        document_id = request.data.get(
            "document_id"
        )

        document = Document.objects.get(
            id=document_id,
            owner=request.user
        )

        conversation = Conversation.objects.create(
            user=request.user,
            document=document
        )

        return Response(
            {
                "conversation_id": conversation.id
            }
        )


class ChatHistoryAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, document_id):

        conversations = Conversation.objects.filter(
            user=request.user,
            document_id=document_id
        )

        serializer = ConversationSerializer(
            conversations,
            many=True
        )

        return Response(
            serializer.data
        )


class ChatMessageAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        conversation_id = request.data.get(
            "conversation_id"
        )

        question = request.data.get(
            "question"
        )

        conversation = Conversation.objects.get(
            id=conversation_id,
            user=request.user
        )

        # Save user's message
        ChatMessage.objects.create(
            conversation=conversation,
            role="user",
            content=question
        )

        # Retrieve relevant document chunks
        chunks = search_similar_chunks(
            question=question,
            document_id=conversation.document.id
        )

        # Generate AI answer
        ai_response = generate_answer(
            question=question,
            chunks=chunks
        )

        # Save AI response
        ChatMessage.objects.create(
            conversation=conversation,
            role="assistant",
            content=ai_response["answer"],
            citations=ai_response["sources"]
        )
        print("AI RESPONSE =", ai_response)

        return Response(
            ai_response
        )