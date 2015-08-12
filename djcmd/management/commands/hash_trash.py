from django.core.management.base import BaseCommand
from djcmd.s3hash import s3_hash_bucket_and_keys
from djcmd.s3hash import extract_sha256_hash
from djcmd.s3hash import extract_cache_hash
from djcmd.utils import exit_error
from djcmd.files_edit import S3HashImageField
from core.s3_hash_models import S3_HASH_MODELS

class Command(BaseCommand):
    def handle(self, *args, **options):
        print "PLEASE REVIEW THE HASH MODEL LIST BEFORE RUNNING THIS SCRIPT..."
        for model in S3_HASH_MODELS:
            print model
        print; print "TYPE yes TO PROCEED"
        raw_in = raw_input('>')
        if not raw_in.lower().strip() == 'yes': exit_error('CANCELLED')

        hashes_in_use = []
        for hash_image_model in S3_HASH_MODELS:
            print ; print hash_image_model
            for field in hash_image_model._meta.fields:
                if not field.__class__ == S3HashImageField: continue
                field_name = field.__repr__()
                field_name = field_name[field_name.find(':') + 1:].replace('>','').strip()
                print hash_image_model.objects.count()
                for obj in hash_image_model.objects.all():
                    obj_hash = extract_sha256_hash(obj.__getattribute__(field_name).__repr__())
                    if obj_hash: hashes_in_use.append(obj_hash)
        print len(hashes_in_use), 'hashes in use'

        thumbnails_in_use = []
        for hash_image_model in S3_HASH_MODELS:
            for image_obj in hash_image_model.objects.all():
                for thumb in image_obj.hash_thumbs():
                    thumbnails_in_use.append(str(thumb).split('.')[0].split('/')[-1])
        print len(thumbnails_in_use), 'thumbnails in use'

        bucket, keys, cache_keys = s3_hash_bucket_and_keys()

        for key_list in [keys, cache_keys]:
            print
            for key in key_list:
                extracted_hash = extract_sha256_hash(key.__repr__())
                if not extracted_hash: continue
                print extracted_hash, 
                if extracted_hash in hashes_in_use:
                    print '... keeping'
                else:
                    print '... deleting'
                    bucket.delete_key(key)

        for key in cache_keys:
            cache_hash = extract_cache_hash(key.__repr__())
            if not cache_hash: continue
            print cache_hash, 
            if cache_hash in thumbnails_in_use:
                print '... keeping'
            else:
                print '... deleting'
                bucket.delete_key(key)
