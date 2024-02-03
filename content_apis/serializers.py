from rest_framework import serializers
from pydash import get

from .models import Content, Author, MediaUrls

class MediaUrlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaUrls
        fields = '__all__'

class ContentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    media_urls = MediaUrlsSerializer(many=True, read_only=True)

    class Meta:
        model = Content
        fields = ['id', 'unique_id', 'unique_uuid', 'origin_unique_id', 'creation_date', 'creation_timestamp',
                  'main_text', 'token_count', 'char_count', 'tag_count', 'origin_platform', 'origin_url',
                  'like_count', 'view_count', 'comment_count', 'author', 'media_urls']

    def get_author(self, obj):
        author = get(obj,'author')
        return {
            'id': get(author,'id'),
            'username': get(author, 'username'),
            'author_id': get(author, 'author_id')
        }

class AuthorSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = '__all__'


class AuthorWiseContentCountSerializer(serializers.ModelSerializer):
    content_count = serializers.IntegerField()

    class Meta:
        model = Author
        fields = ['author_id', 'username', 'content_count']


class PlatformContentCountSerializer(serializers.Serializer):
    origin_platform = serializers.CharField()
    content_count = serializers.IntegerField()

# These serializers. This is kept here for faster implementation. This can be improved.
        
class InternalServerErrorSerializer(serializers.Serializer):
    error = serializers.CharField()

class ContentListQueryParamsSerializer(serializers.Serializer):
    page_no = serializers.IntegerField(required=False)
    page_size = serializers.IntegerField(required=False)