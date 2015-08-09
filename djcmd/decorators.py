def basic_http_auth(f):
    @csrf_exempt
    def wrap(request, *args, **kwargs):
        if 'id_str' in kwargs.keys():
            id_str = kwargs['id_str']
            user_obj = find_user(id_str)
            if user_obj:
                if request.user.is_authenticated():
                    if user_obj.email == request.user.email:
                        return f(request, *args, **kwargs)
                if request.META.get('HTTP_AUTHORIZATION', False):
                    authtype, auth = request.META['HTTP_AUTHORIZATION'].split(' ')
                    auth = base64.b64decode(auth)
                    email, password = auth.split(':')
                    if user_obj.email == email:
                        if authenticate(email=email, password=password):
                            return f(request, *args, **kwargs)
        return JsonHttpError('Authentication failed',status=400) # used to be 401...
    return wrap


def check_user_active(f):
    def wrap(request, *args, **kwargs):
        if 'id_str' in kwargs.keys():
            id_str = kwargs['id_str']
            user_obj = find_user(id_str)
            if user_obj:
                if user_obj.is_active:
                    return f(request, *args, **kwargs)
        #return JsonHttpError('User account has been deactivated')
        return JsonHttpSuccess(msg='User account has been deactivated')
    return wrap
