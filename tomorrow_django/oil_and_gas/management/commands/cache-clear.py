from django.core.management.base import BaseCommand

from ...models import CachedResult


class Command(BaseCommand):
    def handle(self, *args, **options):
        CachedResult.objects.all().delete()
