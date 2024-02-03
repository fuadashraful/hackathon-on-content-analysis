from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .serializers import AuthorSerializer, InternalServerErrorSerializer, ContentListQueryParamsSerializer
from .services import ContentHandleService
from .paginator import StandardResultsSetPagination
from core.utils.query_params import QueryParamsService

class ContentAPIViewset(GenericViewSet):

    @swagger_auto_schema(
        operation_description="Get author and related contents and media urls",
        query_serializer=ContentListQueryParamsSerializer,
        responses={
            200: AuthorSerializer,
            500: InternalServerErrorSerializer,
        },
    )
    def list(self, request: Request) -> Response:

        query_params = QueryParamsService.get_query_params_value(request.query_params)
        content_handle_service = ContentHandleService(query_params)

        authors_with_related_data = content_handle_service.get_contents_with_related_data()

        paginator = StandardResultsSetPagination()

        authors_with_related_data = paginator.paginate_queryset(
            authors_with_related_data,
            request
        )

        serializer = AuthorSerializer(authors_with_related_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
