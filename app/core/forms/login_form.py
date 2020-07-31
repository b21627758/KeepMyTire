from django import forms


class Login(forms.Form):
    email = forms.EmailField(label='email')
    password = forms.CharField(label='password')
