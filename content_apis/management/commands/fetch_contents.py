from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Fetch contents using third party APIS"

    # def add_arguments(self, parser):
    #     parser.add_argument("content_id", nargs="+", type=int)

    def handle(self, *args, **options):

        self.stdout.write(
            self.style.SUCCESS('Content fetched successfully!')
        )