from django import forms
from core.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


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

    def validate_unique(self):
        if get_user_model().objects.filter(email=self.cleaned_data['email']).exists():
            if get_user_model().objects.get(email=self.cleaned_data['email']).is_active:
                raise ValueError('Email Already Exists')
            else:
                return self.cleaned_data['email']
        return self.cleaned_data['email']
