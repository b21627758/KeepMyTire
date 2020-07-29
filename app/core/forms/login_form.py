from django import forms
from core.models import User


class Register(forms.Form):
    email = forms.EmailField()
    password = forms.PasswordInput
