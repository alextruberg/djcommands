from django.core.management.base import BaseCommand
from django.conf import settings
from os.path import exists
from os.path import islink
from os.path import join
from os.path import expanduser
from os import symlink
from os import getcwd
from os import remove
from shutil import rmtree

class Package:
    def __init__(self, git_name, pip_name):
        self.git_name = git_name
        self.pip_name = pip_name

class Command(BaseCommand):
    def handle(self, *args, **options):
        packages = []
        for package in settings.SYMLINK_PACKAGES:
            packages.append(Package(package[0], package[1]))
        for package in packages:
            print package.git_name + '/' + package.pip_name
            site_package_folder = join(getcwd(), 'ENV/lib/python2.7/site-packages/', package.pip_name)
            if exists(site_package_folder):
                function = remove if islink(site_package_folder) else rmtree
                function(site_package_folder)
            symlink(join(expanduser('~'), 'Packages', package.git_name, package.pip_name), site_package_folder)
