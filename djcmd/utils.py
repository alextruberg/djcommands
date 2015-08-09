from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from random import choice
from string import ascii_uppercase
from string import digits
from os import getcwd
from os.path import join
from os.path import split
from os.path import exists
from os import walk
from sys import exit
import json
import base64

def exit_error(msg=None):
    if msg: print msg
    exit()

def combine_and_compress(in_folder, in_ext, out_ext, compress_funct, compile_funct=None, out_folder='core/static'):
    root_folder = join(getcwd(), in_folder)
    text = ''
    all_paths = []
    for root, folders, files in walk(root_folder):
        for filename in files:
            all_paths.append(join(root, filename))
    all_paths.sort()
    for full_path in all_paths:
        filename = split(full_path)[1]
        if full_path.count('/') - 1 == root_folder.count('/'): continue
        if filename.startswith('.'): continue
        if not filename.endswith('.' + in_ext): continue
        if filename.startswith('_'): continue
        text += open(full_path, 'r').read() + '\n'
        print full_path
    print '-' * 60
    compiled = text if not compile_funct else compile_funct(text)
    open(join(out_folder, 'global.' + out_ext), 'w').write(compiled)
    print 'global ' + out_ext + ' written'
    open(join(out_folder, 'global.min.' + out_ext), 'w').write(compress_funct(compiled))
    print 'global ' + out_ext + ' compressed'

def intWithCommas(x):
    if type(x) not in [type(0), type(0L)]:
        raise TypeError("Parameter must be an integer.")
    if x < 0:
        return '-' + intWithCommas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)

def paginate(request,objects,per_page=16):
    page = 1
    if 'page' in request.GET.keys():
        page_str = request.GET['page']
        try:
            page = int(page_str)
        except:
            page = 1
    p = Paginator(objects, per_page)
    page_num = min(page,p.num_pages)
    page_data = p.page(page_num)
    return p, page_data

def safe_url(url):
    if len(url.strip()) == 0: return ''
    if url.startswith('http://'): return url
    if url.startswith('https://'): return url
    return 'http://' + url

def get_quoted_text(whole_string,identifier):
    try:
        index = whole_string.find(identifier)+1+len(identifier)
        rest = whole_string[index:]
        return rest[:rest.find('"')]
    except:
        return ''

def id_generator(size=6, chars=ascii_uppercase + digits): return ''.join(choice(chars) for _ in range(size))

def JsonHttpSuccess(data={}, msg=None, paren=False):
    if msg: data.update({'error': msg})
    full_data = json.dumps(data) if not paren else 'parseUserData(' + json.dumps(data) + ')'
    return HttpResponse(full_data, status=200,content_type="application/json")

def JsonHttpError(msg,status=400):
    print 'error: ' + msg
    r = HttpResponse(json.dumps({'error':msg}),status=status,content_type="application/json")
    if status==401: r['WWW-Authenticate'] = 'Basic realm="bat"'
    return r

def local_http_auth(request,user_obj): # returns True/False
    if request.user.is_authenticated():
        if user_obj.email == request.user.email:
            return True
    if request.META.get('HTTP_AUTHORIZATION', False):
        authtype, auth = request.META['HTTP_AUTHORIZATION'].split(' ')
        auth = base64.b64decode(auth)
        email, password = auth.split(':')
        if user_obj.email == email:
            if authenticate(email=email, password=password):
                return True
    return False
