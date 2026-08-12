from rest_framework import serializers
from .models import Document
from .models import Conversation, ChatMessage
class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = [
            "id",
            "title",
            "file",
            "status",
            "created_at",
             "updated_at",
        ]
        
class ChatMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatMessage

        fields = [
            "id",
            "role",
            "content",
            "citations",
            "created_at"
        ]



class ConversationSerializer(serializers.ModelSerializer):

    messages = ChatMessageSerializer(
        many=True,
        read_only=True
    )


    class Meta:
        model = Conversation

        fields = [
            "id",
            "document",
            "title",
            "messages",
            "created_at",
            "updated_at"
        ]