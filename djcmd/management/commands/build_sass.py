from django.core.management.base import BaseCommand
from djcmd.utils import combine_and_compress
from csscompressor import compress
import sass

class Command(BaseCommand):
    def handle(self, *args, **options):
        combine_and_compress(
                                in_folder='sass',
                                in_ext='scss',
                                out_ext='css',
                                compress_funct=compress,
                                compile_funct=sass.compile_string,
                            )
