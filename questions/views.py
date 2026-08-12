from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Concept, ConceptRelationship



class MindMapAPIView(APIView):

    def get(self, request, document_id):

        concepts = Concept.objects.filter(
            document_id=document_id
        )


        relationships = ConceptRelationship.objects.filter(
            document_id=document_id
        )


        return Response({

            "concepts":[

                {
                    "id":c.id,
                    "name":c.name,
                    "page_number":c.page_number
                }

                for c in concepts

            ],


            "relationships":[

                {
                    "id":r.id,
                    "from_concept_id":r.from_concept.id,
                    "to_concept_id":r.to_concept.id,
                    "relationship":r.relationship
                }

                for r in relationships

            ]

        })