from django.core.management.base import BaseCommand
from django.db import models

class Command(BaseCommand):
    def handle(self, *args, **options):
        for model in models.get_models(include_auto_created=False):
            print model
        