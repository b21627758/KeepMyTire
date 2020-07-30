from django import forms
from core.models import User
from django.contrib.auth.forms import UserCreationForm


class Register(UserCreationForm):
    class Meta:
        model = User
        fields = {
            'first_name',
            'last_name',
            'date_of_birth',
            'email',
            'phone_num',
            'password1',
            'password2'
        }
