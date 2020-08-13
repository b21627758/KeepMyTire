from django import forms
from core.models import Car


class CreateCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = {
            'color',
            'brand',
            'model'
        }

        exclude = ('owner', 'plate')

    plate = forms.CharField(max_length=11)
