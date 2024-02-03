from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Content, Author, MediaUrls

from .serializers import ContentSerializer, AuthorSerializer

class ContentAPIViewset(GenericViewSet):

    def list(self, request: Request) -> Response:

        authors_with_related_data = Author.objects.prefetch_related('contents')
        serializer = AuthorSerializer(authors_with_related_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
