from django import forms
from core import models


class BookingForm(forms.ModelForm):
    """Form for reservation"""

    class Meta:
        model = models.Reservation
        fields = {
            'date',
            'time',
            'process',  # 0-Just Store Tire, 1-Just Change Tire And Do Not Store, 2-Change And Store Tire
                        # 3-Just Sell Tire, 4-Sell And Change Tire,5-Sell, Change And Store Changed Tire
                        # 6-Just Rot Balance
            'notify'
        }

        exclude = ('customer',)
