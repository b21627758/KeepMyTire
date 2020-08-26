from django import forms
from core import models


class TireOnCar(forms.Form):
    """Move Tire To Car Form"""

    car = forms.CharField(max_length=20)
    tire = forms.CharField(max_length=10)
