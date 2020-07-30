from django import forms


class Login(forms.Form):
    email = forms.EmailField()
    password = forms.PasswordInput()
