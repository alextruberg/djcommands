from django.core.management.base import BaseCommand
from djcmd.s3hash import s3_hash_bucket_and_keys
from djcmd.s3hash import extract_sha256_hash
from djcmd.utils import exit_error
from djcmd.files_edit import S3HashImageField
from console.models import HeroSlide
from opportunities.models import Opportunity

class Command(BaseCommand):
    def handle(self, *args, **options):
        print "PLEASE REVIEW THE HASH MODEL LIST BEFORE RUNNING THIS SCRIPT..."
        print "TYPE yes TO PROCEED"
        raw_in = raw_input('>')
        if not raw_in.lower().strip() == 'yes': exit_error('CANCELLED')
        hashes_in_use = []
        hash_image_models = [ HeroSlide, Opportunity ]
        for hash_image_model in hash_image_models:
            for field in hash_image_model._meta.fields:
                if not field.__class__ == S3HashImageField: continue
                field_name = field.__repr__()
                field_name = field_name[field_name.find(':') + 1:].replace('>','').strip()
                for obj in hash_image_model.objects.all():
                    obj_hash = extract_sha256_hash(obj.__getattribute__(field_name).__repr__())
                    if obj_hash: hashes_in_use.append(obj_hash)
        print hashes_in_use
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
