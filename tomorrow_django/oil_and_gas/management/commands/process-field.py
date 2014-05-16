import ast

from django.core.management.base import BaseCommand

from ...tasks import process_field


class Command(BaseCommand):
    def handle(self, *args, **options):
        options = ast.literal_eval(args[0])
        process_field(options)
