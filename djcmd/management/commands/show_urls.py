from django.core.management.base import BaseCommand
from core import urls

def show_urls(urllist, depth=0):
    for entry in urllist:
        print "  " * depth, entry.regex.pattern, 
        try:
            print entry._callback_str
        except:
            print '<no callback>'
        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, depth + 1)

class Command(BaseCommand):
    def handle(self, *args, **options):
        show_urls(urls.urlpatterns)
