from rest_framework.viewsets import GenericViewSet
from rest_framework.request import Request
from rest_framework.response import Response


class ContentAPIViewset(GenericViewSet):

    def list(self, request: Request) -> Response:
        return Response({
             "author": {
                "id": 919301,
                "username": "stuffedddd"
            },
            "context": {
                "main_text": "@pizzahuteg",
                "token_count": 1,
                "char_count": 11,
                "tag_count": 1
            },
        })