from django.core.management.base import BaseCommand
from os import walk
from os import getcwd
from os.path import join

class AppCommandList:
    def __init__(self):
        self.data = []
    def add_item(self,app,command):
        self.data.append(AppCommand(app,command))
    def sort_by_command(self):
        self.data.sort(cmp=self.sort_method_command)
    def sort_method_command(self,a,b):
        if a.command < b.command: return -1
        if a.command > b.command: return  1
        return 0
    def print_all(self):
        for app_command in self.data:
            print app_command.command.ljust(30,' '), app_command.app

class AppCommand:
    def __init__(self,app,command):
        self.app = app
        self.command = command

class Command(BaseCommand):
    def handle(self, *args, **options):
        all_commands = AppCommandList()
        for root, folders, files in walk(getcwd()):
            for file_ in files:
                full_path = join(root, file_)
                if "/management/" in full_path and \
                   "/commands/" in full_path and \
                   "/ENV/" not in full_path:
                    app_name = full_path.replace(getcwd()+'/','')
                    app_name = app_name[:app_name.find('/')]
                    command_name = full_path[full_path.rfind('/')+1:]
                    if not command_name == "__init__.py" and command_name.endswith('.py'):
                        all_commands.add_item(app_name,command_name)
        all_commands.sort_by_command()
        all_commands.print_all()
