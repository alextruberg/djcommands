from django.core.management.base import BaseCommand
from djcmd.user_utils import find_user
from djcmd.utils import exit_error

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not len(args) == 2: exit_error("usage: change_pw username/id password")
        user_id = args[0]
        password = args[1]
        user = find_user(user_id)
        if not user: exit_error('Could not locate the user...')
        print user
        user.set_password(password)
        user.save()
        print "password changed"
