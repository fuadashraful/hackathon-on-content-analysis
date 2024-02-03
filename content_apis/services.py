from .models import  Content
from core.utils.query_params import QueryParamConstant
from django.db.models import F

class ContentHandleService(object):

    __slots__ = ('query_params')

    def __init__(self, query_params):
        self.query_params = query_params
    def get_contents_with_related_data(self):
        authors_with_related_data = Content.objects.prefetch_related('media_urls')

        unique_id = self.query_params.get(QueryParamConstant.UNIQUE_ID)

        if unique_id:
            authors_with_related_data = authors_with_related_data.filter(unique_id=unique_id)
        
        return authors_with_related_data

