from django.core.management.base import BaseCommand
from os import remove
from os import listdir
from os.path import join
from os.path import isfile
from os.path import isdir
from core import settings

def remove_pycs(folder):
    for file_or_folder in listdir(folder):
        full_path=join(folder,file_or_folder)
        if isfile(full_path):
            if file_or_folder.endswith('.pyc'):
                try:
                    print "removing: " + full_path
                    remove(full_path)
                except:
                    pass
        if isdir(full_path):
            remove_pycs(full_path)

class Command(BaseCommand):
    def handle(self, *args, **options):
        remove_pycs(settings.BASE_DIR)
