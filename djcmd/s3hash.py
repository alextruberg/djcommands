from django.conf import settings
from core.settings import AWS_ACCESS_KEY_ID
from core.settings import AWS_SECRET_ACCESS_KEY
from core.settings import AWS_STORAGE_BUCKET_NAME
from imagekit.processors import ResizeToFill
from imagekit.processors import ResizeToFit
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import re
import hashlib

img_kwargs = {}
scopes = ['xs', 'sm', 'md', 'lg']
for size in map(lambda scope: 'size_' + scope, scopes):
    for qual in map(lambda scope: 'qual_' + scope, scopes):
        for ratio in ['aspect', 'square']:
            name = size + '_' + qual + '_' + ratio
            img_kwargs[name] = {
                'processors':[ResizeToFill(settings.IMG[size], settings.IMG[size])] if ratio=='square' else [ResizeToFit(height=settings.IMG[size])],
                'format':'JPEG',
                'options':{'quality': settings.IMG[qual]}
            }

def get_file_hash(binary_contents):
    return hashlib.sha256(binary_contents).hexdigest()    

def extract_sha256_hash(in_str):
    matches = re.compile('[A-Fa-f0-9]{64}').findall(in_str)
    if not len(matches): return None
    return matches[0]

def extract_cache_hash(in_str):
    cache_hash_split = in_str.split('/')
    if not(len(cache_hash_split)): return None
    matches = re.compile('[A-Fa-f0-9]{32}').findall(cache_hash_split[-1])
    if not len(matches): return None
    return matches[0]

def s3_hash_bucket_and_keys():
    print 'downloading image hash keys from S3...'
    conn = S3Connection(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(AWS_STORAGE_BUCKET_NAME)
    return (
        bucket,
        bucket.list(settings.S3_JPEG_HASH_PATH),
        bucket.list(settings.S3_JPEG_HASH_CACHE_PATH),
    )

def s3_hash_list():
    matches = []
    for key in s3_hash_bucket_and_keys()[1]:
        extracted_hash = extract_sha256_hash(key.__repr__())
        if extracted_hash: matches.append(extracted_hash)
    return matches

def s3_cache_urls(obj):
    ret_dict = {}
    for thumb in obj.s3_hash_strings():
        exec_str = 'ret_dict["' + thumb + '"] = "' + settings.AWS_S3_ROOT + '" + str(obj.' + thumb + ')'
        exec(exec_str)
    return ret_dict

def s3_hash_thumbs(obj):
    ret_list = []
    for thumb in obj.s3_hash_strings(): exec("ret_list.append(obj." + thumb + ")")
    return ret_list
