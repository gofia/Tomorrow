from django.core.management.base import BaseCommand

from ...hubbert import HubbertBacktest


class Command(BaseCommand):
    def handle(self, *args, **options):
        country = "NO"
        if len(args) > 0 and args[0] == "UK":
            country = "UK"
        HubbertBacktest.run(country)
