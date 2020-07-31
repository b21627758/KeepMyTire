from django.contrib.auth import get_user_model


class EmailBackend(object):

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = get_user_model().objects.get(email=username)
        except get_user_model().MultipleObjectsReturned:
            user = get_user_model().objects.filter(email=username).order_by('id').first()
        except get_user_model().DoesNotExist:
            return None

        if getattr(user, 'is_active') and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
