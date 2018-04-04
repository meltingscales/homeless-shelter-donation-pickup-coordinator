from django import forms
from django.forms import ModelForm

from donator.models import Home
from .models import Org


class OrgForm(ModelForm):
    class Meta:
        model = Org
        exclude = ('location',)


class HomeSearchForm(forms.Form):
    """For searching a list of Homes."""

    class Meta:
        model = Home
        default_miles = 5


    distance = forms.NumberInput(attrs={
        'step': 0.5,
    })
