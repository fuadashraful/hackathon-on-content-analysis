from rest_framework.viewsets import GenericViewSet
from rest_framework.request import Request
from rest_framework.response import Response


class ContentAPIViewset(GenericViewSet):

    def list(self, request: Request) -> Response:
        return Response({
            "name": "Test response"
        })