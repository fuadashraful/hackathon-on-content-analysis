import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

import logging
from pydash import get
from rest_framework import status
import time
         
RUN_FOREVER = True
headers = {
    'x-api-key':  settings.HACK_API_KEY
}

def retry_decorator(max_attempts=3, wait_seconds=5):

    def decorator(func):
        def wrapper(*args, **kwargs):
            response = None
            for _ in range(max_attempts):
                try:
                    response = func(*args, **kwargs)
                    if get(response,'status_code') != status.HTTP_200_OK:
                        time.wait(wait_seconds * 1000)
                    else:
                        return response

                except Exception as e:
                    logging.error(f"Error while fetching {e}")

            return response

        return wrapper

    return decorator


class Command(BaseCommand):
    help = "Fetch contents using third party APIS"

    def get_content_data(self, page):
        api_endpoint = f"{settings.API_ROOT}?{page}=1"
        response = requests.get(api_endpoint, headers=headers)

        return response

    def handle(self, *args, **options):


        while RUN_FOREVER:
            
            next_page = 1

            while next_page:
                
                try:
                    response = self.get_content_data(next_page)

                    if get(response, 'status_code') == status.HTTP_200_OK:
                        response_data = response.json()

                        self.stdout.write(
                            self.style.SUCCESS(f'page {next_page} data{response_data}')
                        )

                        next_page = get(response_data, 'next')
                    else:
                        next_page+=1

                except Exception as e:
                    next_page = None
                    logging.error(f"Got the error while fetching {e}")