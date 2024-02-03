from .models import  Author
from core.utils.query_params import QueryParamConstant

class ContentHandleService(object):

    __slots__ = ('query_params')

    def __init__(self, query_params):
        self.query_params = query_params
    def get_contents_with_related_data(self):
        authors_with_related_data = Author.objects.prefetch_related('contents')

        author_id = self.query_params.get(QueryParamConstant.AUTHOR_ID)
        page_no = self.query_params.get(QueryParamConstant.PAGE_NO)
        page_size = self.query_params.get(QueryParamConstant.PAGE_SIZE)

        if author_id:
            authors_with_related_data = authors_with_related_data.filter(author_id=author_id)
        
        return authors_with_related_data

