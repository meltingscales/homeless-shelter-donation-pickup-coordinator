from django import forms
from django.forms import ModelForm

from .models import Org, OrgItems


class OrgForm(ModelForm):
    class Meta:
        model = Org
        exclude = ('location',)


class HomeSearchForm(forms.Form):
    """For searching a list of Homes."""

    class Meta:
        default_miles = 5

    miles = forms.FloatField(initial=Meta.default_miles)

    def is_valid(self):
        form_data = self.data

        print(form_data)

        print("asking if HomeSearchForm is valid.")

        if 'miles' in self.data:
            print("Miles!")
            try:
                var = float(self.data['miles'])
            except ValueError:
                self.add_error('miles', 'Miles must be a number!')
                print(self.errors)
                return False


        return super(HomeSearchForm, self).is_valid()


class OrgItemsForm(ModelForm):
    class Meta:
        model = OrgItems
        exclude = ()
