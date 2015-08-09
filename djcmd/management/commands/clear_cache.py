from django.core.management.base import BaseCommand
from django.core.cache import cache

class Command(BaseCommand):
    def handle(self, *args, **options):
        print cache.keys('*')
        print "CLEARING CACHE..."
        cache.clear()
        print cache.keys('*')

