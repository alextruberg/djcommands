from django.core.management.base import BaseCommand
from djcmd.s3hash import s3_hash_bucket_and_keys
from djcmd.s3hash import extract_sha256_hash
from djcmd.s3hash import extract_cache_hash
from djcmd.utils import exit_error
from djcmd.files_edit import S3HashImageField
from core.s3_hash_models import S3_HASH_MODELS

class Command(BaseCommand):
    def handle(self, *args, **options):
        bucket, keys, cache_keys = s3_hash_bucket_and_keys()
        existing_cache_hashes = []
        for key in cache_keys:
            cache_hash = extract_cache_hash(key.__repr__())
            if not cache_hash: continue
            existing_cache_hashes.append(cache_hash)

        for hash_image_model in S3_HASH_MODELS:
            for image_obj in hash_image_model.objects.all():
                for thumb in image_obj.hash_thumbs():
                    thumb_hash = str(thumb).split('.')[0].split('/')[-1]
                    if not(len(thumb_hash.strip())): continue
                    print thumb_hash,
                    if thumb_hash in existing_cache_hashes:
                        print 'already exists...'
                    else:
                        print 'generating...'
                        thumb.generate()
