from django import forms
from core.models import ConditionReport


class CreateConditionReportForm(forms.ModelForm):
    class Meta:
        model = ConditionReport
        fields = {
            'condition',
            'erl',
            'tire'
        }

        exclude = ('reporter', 'date', 'time')
