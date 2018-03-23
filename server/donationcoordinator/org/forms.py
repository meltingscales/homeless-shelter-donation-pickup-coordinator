from django import forms
from django.forms import ModelForm

from .models import Org


class OrgForm(ModelForm):
    class Meta:
        model = Org
        exclude = ()


class HomeSearchForm(ModelForm):
    """For searching a list of Homes."""
    distance = forms.NumberInput()
