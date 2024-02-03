from django.db import models



class Author(models.Model):
    author_id = models.IntegerField()
    username = models.CharField(max_length=100)


class Content(models.Model):
    unique_id = models.IntegerField()
    unique_uuid = models.CharField(max_length=100)
    origin_unique_id = models.CharField(max_length=100)
    creation_date= models.DateTimeField()
    creation_timestamp = models.DateTimeField()
    main_text = models.TextField()
    token_count = models.IntegerField()
    char_count = models.IntegerField()
    tag_count = models.IntegerField()
    origin_platform = models.CharField(max_length=100)
    origin_url = models.CharField(max_length=1000)
    like_count = models.IntegerField()
    view_count = models.IntegerField()
    comment_count = models.IntegerField()
    
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class MediaUrls(models.Model):
    url = models.CharField(max_length=1000)
    media_type = models.CharField(max_length=1000)
    
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
