from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import AuthorSerializer
from .services import ContentHandleService

class ContentAPIViewset(GenericViewSet):

    def list(self, request: Request) -> Response:

        content_handle_service = ContentHandleService()

        authors_with_related_data = content_handle_service.get_contents_with_related_data()

        serializer = AuthorSerializer(authors_with_related_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
