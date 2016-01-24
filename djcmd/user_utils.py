from django.conf import settings

def get_user_model():
    user_model_text = settings.AUTH_USER_MODEL
    if user_model_text == 'auth.User':
        from django.contrib.auth.models import User
        return User
    if user_model_text == 'user.R2SUser':
        from user.models import R2SUser
        return R2SUser
    return None

def find_user(identifier, find_many=False, partial_match=False, param_list=['id', 'email', 'name', 'username']):
    model = get_user_model()
    users = []
    for param in param_list:
        try:
            users += model.objects.filter(**{ param + ('__icontains' if partial_match and not param == 'id' else '__iexact'): str(identifier) })
        except:
            pass
    if not find_many: return users[0] if len(users) else None
    return list(set(users))

def get_random_user(): return get_user_model().objects.order_by('?')[0]
