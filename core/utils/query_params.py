
class QueryParamConstant:
    PAGE_NO = 'page_no'
    PAGE_SIZE = 'page_size'
    AUTHOR_ID = 'author_id'

    DEFAULT_PAGE_NO = 1
    DEFAULT_PAGE_SIZE = 10

class QueryParamsService:
    @staticmethod
    def get_query_params_value(query_params):
        query_params = {
            QueryParamConstant.PAGE_NO: query_params.get(QueryParamConstant.PAGE_NO, QueryParamConstant.DEFAULT_PAGE_NO),
            QueryParamConstant.PAGE_SIZE : query_params.get(QueryParamConstant.PAGE_SIZE, QueryParamConstant.DEFAULT_PAGE_SIZE),
            QueryParamConstant.AUTHOR_ID: query_params.get(QueryParamConstant.AUTHOR_ID),
        }

        return query_params
