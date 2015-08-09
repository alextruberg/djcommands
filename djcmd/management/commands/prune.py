from django.core.management.base import BaseCommand
from os import getcwd
from os import walk
from os.path import join

class Command(BaseCommand):
    def handle(self, *args, **options):
        all_code = ''
        for root, folders, files in walk(getcwd()):
            for file_ in files:
                full_path = join(root,file_)
                if full_path.endswith('.py') or full_path.endswith('.html'):
                    all_code += open(full_path,'r').read() + '\n'

        print len(all_code)

        all_snippets = []
        for root, folders, files in walk(getcwd()):
            for file_ in files:
                if file_.endswith('.html'):
                    if all_code.count(file_) == 0:
                        print str(all_code.count(file_)).rjust(3,' '), file_
