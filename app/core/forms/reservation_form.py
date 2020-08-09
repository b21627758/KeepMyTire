from django import forms
from core import models


class BookingForm(forms.ModelForm):
    """Form for reservation"""

    class Meta:
        model = models.Reservation
        fields = {
            'date',
            'time',
            'process',
            'notify'
        }

        exclude = ('customer', 'staff')

    staff = forms.CharField(max_length=255)
