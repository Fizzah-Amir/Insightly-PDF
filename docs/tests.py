from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Document

User=get_user_model()

class DocumentTest(TestCase):
    def setUp(self):
        self.user=User.objects.create_user(
             username="testuser",
            password="testpass123"
        )
    def test_document_created(self):
        document=Document.objects.create(
            owner=self.user,
            file="sample.pdf"
        )
    
        self.assertEqual(document.owner, self.user)
        self.assertEqual(
            document.status,
            Document.Status.UPLOADED
        )
# Create your tests here.
