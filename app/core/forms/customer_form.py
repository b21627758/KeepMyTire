from django import forms
from django.contrib.auth import models , get_user_model
from django.contrib.auth.forms import UserCreationForm


class CreateCustomerForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = {
            'first_name',
            'last_name',
            'email',
            'phone_num'
        }
