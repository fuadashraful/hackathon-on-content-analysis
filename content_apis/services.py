from .models import  Author


class ContentHandleService(object):
    def get_contents_with_related_data(self):
        author_id = None

        authors_with_related_data = Author.objects.prefetch_related('contents')

        if author_id:
            authors_with_related_data = authors_with_related_data.filter(author_id=author_id)
        
        return authors_with_related_data

