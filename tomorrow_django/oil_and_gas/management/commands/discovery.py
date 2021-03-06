from django.core.management.base import BaseCommand

from ...tasks import discovery_countries


class Command(BaseCommand):
    def handle(self, *args, **options):
        country = "NO"
        if len(args) > 0 and args[0] == "UK":
            country = "UK"
        discovery_countries(country)
