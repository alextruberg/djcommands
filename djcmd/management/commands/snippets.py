from django.core.management.base import BaseCommand
from os import walk
from os import getcwd

def sort_method_file(a,b):
    if a['file'] < b['file']: return -1
    if a['file'] > b['file']: return  1
    return 0

class Command(BaseCommand):
    def handle(self, *args, **options):
        all_snippets = []
        for root, folders, files in walk(getcwd()):
            for file_ in files:
                if 'templates/snippets' in root:
                    app = root.replace(getcwd(),'').replace('templates/snippets','').replace('/','')
                    all_snippets.append({'app':app, 'file':file_})
        all_snippets.sort(cmp=sort_method_file)
        for snippet in all_snippets:
            print snippet['file'].ljust(40,' ') + snippet['app']
