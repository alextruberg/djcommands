from django.core.management.base import BaseCommand
from os import system

class Command(BaseCommand):
    def handle(self, *args, **options):
        system('heroku pg:backups')