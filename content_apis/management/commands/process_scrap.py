from django.core.management.base import BaseCommand, CommandError

from content_apis.models import UserInfo, VideoUrl, PhotoUrl
from pydash import get

from .scrap_data import SCRAPED_DATA
import requests

from content_apis.serializers import UserInfoSerializer

class Command(BaseCommand):
    help = "Add scraped data"

    def handle(self, *args, **options):
        api_endpoint = 'https://3c9pj1-ip-202-84-41-237.tunnelmole.net/api/'

        response = requests.get(api_endpoint)

        scrapped_data = response.json()

        new_ids = [
            data.get("user_id") for data in scrapped_data
        ]

        existing_user_infos = UserInfo.objects.filter(user_id__in=new_ids)

        serializer = UserInfoSerializer(existing_user_infos, many=True)

        existing_user_ids = [
            user_info.get("user_id") for user_info in serializer.data
        ]


        for data in scrapped_data:

            if data.get("user_id") not in existing_user_ids:
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