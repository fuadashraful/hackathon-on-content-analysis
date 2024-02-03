from core.utils.query_params import QueryParamConstant
from django.db.models import F
from django.db.models import Count

from .models import  Content, Author, MediaUrls
from .serializers import (
    AuthorWiseContentCountSerializer,
    PlatformContentCountSerializer
)

class ContentHandleService(object):

    __slots__ = ('query_params')

    def __init__(self, query_params=None):
        self.query_params = query_params

    def get_contents_with_related_data(self):
        authors_with_related_data = Content.objects.prefetch_related('media_urls')

        unique_id = self.query_params.get(QueryParamConstant.UNIQUE_ID)

        if unique_id:
            authors_with_related_data = authors_with_related_data.filter(unique_id=unique_id)
        
        return authors_with_related_data



    def get_content_statistics(self):
        #Writing all statistics here in production it should be handled more precisely
        data = {}
    
        author_content_count = Author.objects.annotate(content_count=Count('contents')).all()
        serializer = AuthorWiseContentCountSerializer(author_content_count, many=True)

        data["author_wise_content_count"] = serializer.data

        platform_content_count = Content.objects.values('origin_platform').annotate(content_count=Count('id')).all()

        serializer = PlatformContentCountSerializer(platform_content_count, many=True)

        data["platform_wise_content_count"] = serializer.data

        return data