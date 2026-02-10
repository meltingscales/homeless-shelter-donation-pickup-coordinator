from django import forms
from django.forms import ModelForm

from .models import Org, OrgItems


class OrgForm(ModelForm):
    class Meta:
        model = Org
        exclude = ('location', 'items')


class HomeSearchForm(forms.Form):
    """For searching a list of Homes."""

    class Meta:
        default_miles = 5

    miles = forms.FloatField(initial=Meta.default_miles)

    def miles_valid(self):
        if 'miles' in self.data:
            try:
                var = float(self.data['miles'])
                return True
            except ValueError:
                self.add_error('miles', 'Miles must be a number!')
                return False

    def is_valid(self):

        if not self.miles_valid():
            return False

        return super(HomeSearchForm, self).is_valid()


class OrgItemsForm(ModelForm):
    class Meta:
        model = OrgItems
        exclude = ()
