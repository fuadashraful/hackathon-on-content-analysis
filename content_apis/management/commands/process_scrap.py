from django.core.management.base import BaseCommand, CommandError

from content_apis.models import UserInfo, VideoUrl, PhotoUrl
from pydash import get

from .scrap_data import SCRAPED_DATA

class Command(BaseCommand):
    help = "Add scraped data"

    def handle(self, *args, **options):
        for data in SCRAPED_DATA:
            user_info = UserInfo(
                user_id=data.get("user_id"),
                username=data.get("username"),
                full_name=data.get("full_name"),
                profile_pic_url=data.get("profile_pic_url")
            )

            user_info.save()

            video_urls = data.get("video_url", [])

            video_url_instances = [
                VideoUrl(url=video_url, user=user_info)
                for video_url in video_urls
            ]

            VideoUrl.objects.bulk_create(video_url_instances)

            photo_urls = data.get("photo_url", [])
        
            photo_url_instances = [
                PhotoUrl(url=photo_url, user=user_info)
                for photo_url in photo_urls
            ]
        
            PhotoUrl.objects.bulk_create(photo_url_instances)