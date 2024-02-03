from rest_framework import serializers

from .models import Content, Author, MediaUrls

class MediaUrlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaUrls
        fields = '__all__'

class ContentSerializer(serializers.ModelSerializer):
    media_urls = MediaUrlsSerializer(many=True, read_only=True)

    class Meta:
        model = Content
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = '__all__'


# Server error serializer. This is kept here for faster implementation. This can be improved.
        
class InternalServerErrorSerializer(serializers.Serializer):
    error = serializers.CharField()

class ContentListQueryParamsSerializer(serializers.Serializer):
    page_no = serializers.IntegerField(required=False)
    page_size = serializers.IntegerField(required=False)