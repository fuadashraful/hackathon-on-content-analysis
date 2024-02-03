from core.utils.query_params import QueryParamConstant
from django.db.models import F
from django.db.models import Count, Sum

from .models import  Content, Author, MediaUrls
from .serializers import (
    AuthorWiseContentCountSerializer,
    PlatformContentCountSerializer,
    ContentLikeCommentViewSumSerializer,
    AuthorSerializer,
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

        all_content_like_comment_view_sum = Content.objects.aggregate(
            total_likes=Sum('like_count'),
            total_comments=Sum('comment_count'),
            total_views=Sum('view_count')
        )

        serializer = ContentLikeCommentViewSumSerializer(all_content_like_comment_view_sum)

        data["all_content_like_comment_view_sum"] = serializer.data

        # Due to time constraint writing some queries in this method. In reallime it could be more simple
        author_with_max_content = Author.objects.annotate(content_count=Count('contents')).order_by('-content_count').first()
        
        serializer = AuthorSerializer(author_with_max_content)

        data["author_with_max_content"] = {**serializer.data, "content_count": author_with_max_content.content_count}

        author_with_min_content = Author.objects.annotate(content_count=Count('contents')).order_by('content_count').first()
        
        serializer = AuthorSerializer(author_with_min_content)

        data["author_with_min_content"] = {**serializer.data, "content_count": author_with_min_content.content_count}

        return data