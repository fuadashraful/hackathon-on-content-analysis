from django.db import models


class Author(models.Model):
    author_id = models.IntegerField(null=True)
    username = models.CharField(max_length=100, null=True, blank=True)


class Content(models.Model):
    unique_id = models.IntegerField(null=True)
    unique_uuid = models.CharField(max_length=100, null=True, blank=True)
    origin_unique_id = models.CharField(max_length=100, null=True, blank=True)
    creation_date= models.DateTimeField(null=True, blank=True)
    creation_timestamp = models.DateTimeField(null=True, blank=True)
    main_text = models.TextField(null=True, blank=True)
    token_count = models.IntegerField(null=True)
    char_count = models.IntegerField(null=True)
    tag_count = models.IntegerField(null=True)
    origin_platform = models.CharField(max_length=100, null=True, blank=True)
    origin_url = models.CharField(max_length=1000, null=True, blank=True)
    like_count = models.IntegerField(null=True)
    view_count = models.IntegerField(null=True)
    comment_count = models.IntegerField(null=True)
    
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='contents')


class MediaUrls(models.Model):
    url = models.CharField(max_length=1000, null=True, blank=True)
    media_type = models.CharField(max_length=1000, null=True, blank=True)
    
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='media_urls')
