from django import forms
from core.models import User


class Register(forms.ModelForm):
    class Meta:
        model = User
        fields = {
            'first_name',
            'last_name',
            'date_of_birth',
            'email',
            'phone_num'
        }
