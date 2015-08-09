from django.core.management.base import BaseCommand
from djcmd.utils import combine_and_compress
import uglipyjs

class Command(BaseCommand):
    def handle(self, *args, **options):
        combine_and_compress(
                                in_folder='js',
                                in_ext='js',
                                out_ext='js',
                                compress_funct=uglipyjs.compile,
                                compile_funct=None,
                            )
