import requests
from django.conf import settings
from django.core.management.base import BaseCommand

import logging
from pydash import get
from rest_framework import status
import time

from content_apis.models import Content, Author, MediaUrls

#These docorator and constant stuffs should be in seperate file in normal dev phase        
RUN_FOREVER = True
FIVE_MIN_INTERVAL = 5 * 60 * 1000
headers = {
    'x-api-key':  settings.HACK_API_KEY
}

def retry_decorator(max_attempts=3, wait_seconds=5):

    def decorator(func):
        def wrapper(*args, **kwargs):
            response = None
            for try_no in range(max_attempts):
                try:
                    logging.info(f"Try no {try_no+1}")
                    response = func(*args, **kwargs)
                    if get(response,'status_code') != status.HTTP_200_OK:
                        time.sleep(wait_seconds * 1000)
                    else:
                        return response

                except Exception as e:
                    logging.error(f"Error while fetching {e}")

            return response

        return wrapper

    return decorator


class Command(BaseCommand):
    help = "Fetch contents using third party APIS"

    @retry_decorator()
    def get_content_data(self, page):
        api_endpoint = f"{settings.API_ROOT}?page={page}"
        response = requests.get(api_endpoint, headers=headers)

        return response

    def create_or_get_existing_author(self, content):
        author_id = get(content, 'author.id')

        existing_author = Author.objects.filter(author_id=author_id).first()

        if not existing_author:
            existing_author = Author(
                author_id = get(content, 'author.id'),
                username = get(content, 'author.username')
            )

            existing_author.save()

        return existing_author

    def create_content(self, content, author):
        created_content = Content(
            unique_id = get(content, 'unique_id'),
            unique_uuid = get(content, 'unique_uuid'),
            origin_unique_id = get(content, 'origin_unique_id'),
            creation_date= get(content, 'creation_info.created_at'),
            creation_timestamp = get(content, 'creation_info.timestamp'),
            main_text = get(content, 'context.main_text'),
            token_count = get(content, 'context.token_count'),
            char_count = get(content, 'context.char_count'),
            tag_count = get(content, 'context.tag_count'),
            origin_platform = get(content, 'origin_details.origin_platform'),
            origin_url = get(content, 'origin_details.origin_url'),
            like_count = get(content, 'stats.digg_counts.likes.count'),
            view_count = get(content, 'stats.digg_counts.views.count'),
            comment_count = get(content, 'stats.digg_counts.comments.count'),
            author=author
        )

        created_content.save()

        return created_content
    
    def create_media_urls(self, content, created_content):
        media_urls = get(content, "media.urls")
        media_type = get(content, "media.media_type")

        media_url_instances = [
            MediaUrls(
               url=media_url,
               media_type= media_type,
               content=created_content
            ) for media_url in media_urls
        ]

        MediaUrls.objects.bulk_create(media_url_instances)

    def insert_content_and_related_data_to_db(self, content):
        # We could move keys to constant and make robust function to get data in normal industry practice


        author = self.create_or_get_existing_author(content)
        created_content = self.create_content(content, author)

        self.create_media_urls(content, created_content)

        #Media data


    def insert_content_data(self, contents):

        unique_ids = [get(content, 'unique_id') for content in contents]

        content_instances = Content.objects.filter(unique_id__in=unique_ids)

        inserted_content_ids = [content_instance.unique_id for content_instance in content_instances]

        for content in contents:
            if get(content, 'unique_id') not in inserted_content_ids:
                self.insert_content_and_related_data_to_db(content)

    def handle(self, *args, **options):

        while RUN_FOREVER: 
            next_page = 1

            while next_page:
                try:
                    response = self.get_content_data(next_page)

                    if get(response, 'status_code') == status.HTTP_200_OK:
                        response_data = response.json()

                        self.insert_content_data(get(response_data, 'data', []))

                        self.stdout.write(
                            self.style.SUCCESS(f'Synced data for {next_page}')
                        )
                        next_page = get(response_data, 'next')
                    else:
                        next_page+=1

                except Exception as e:
                    next_page = None
                    logging.error(f"Got the error while fetching {e}")
        
            self.stdout.write(
                self.style.SUCCESS('Waiting 5 min for next sync request')
            )

            time.sleep(FIVE_MIN_INTERVAL)