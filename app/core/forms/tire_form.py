from django import forms
from core import models


class CreateTireForm(forms.ModelForm):
    """Record customers tire"""

    class Meta:
        model = models.Tire
        fields = {
            'brand',
            'model',
            'size',
            'usage'
        }


class CreateNewTireForm(forms.ModelForm):
    """Record unused tire"""

    class Meta:
        model = models.NewTire
        fields = {
            'brand',
            'model',
            'size',
            'usage',
            'p_num',
            'price',
            'm_date'
        }