from django.core.management.base import BaseCommand

from ...tasks import discovery_countries


class Command(BaseCommand):
    def handle(self, *args, **options):
        discovery_countries("NO")
