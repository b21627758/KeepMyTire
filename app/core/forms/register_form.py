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

    def clean(self):
        cleaned_data = super(Register, self).clean()
        password = cleaned_data.get('password1')
        email = cleaned_data.get('email')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        phone_num = cleaned_data.get('phone_num')
        birth_date = cleaned_data.get('date_of_birth')
        if len(email) <= 0:
            msg = 'Need Valid Password'
            self.add_non_field_errors('first_name', msg)
        if len(first_name) <= 0:
            msg = 'Need First Name'
            self.add_non_field_errors('first_name', msg)
        if len(last_name) <= 0:
            msg = 'Need Last Name'
            self.add_non_field_errors('first_name', msg)
        """if phone_num is not None:
            msg = 'Need Phone Number'
            self.add_error('phone_num', msg)"""
        if not birth_date:
            msg = 'Need Birth Date'
            self.add_error('date_of_birth', msg)
        # check for min length
        min_length = 8
        if len(password) < min_length:
            msg = 'Password must be at least %s characters long.' % (str(min_length))
            self.add_error('password1', msg)

        # check for digit
        if sum(c.isdigit() for c in password) < 1:
            msg = 'Password must contain at least 1 number.'
            self.add_error('password1', msg)

        # check for uppercase letter
        if not any(c.isupper() for c in password):
            msg = 'Password must contain at least 1 uppercase letter.'
            self.add_error('password1', msg)

        # check for lowercase letter
        if not any(c.islower() for c in password):
            msg = 'Password must contain at least 1 lowercase letter.'
            self.add_error('password1', msg)

        password_confirm = cleaned_data.get('password2')

        if password and password_confirm:
            if password != password_confirm:
                msg = "The two password fields must match."
                self.add_error('password2', msg)
        return cleaned_data
