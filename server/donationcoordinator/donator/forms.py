from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Items, Home, Profile


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ()


class HomeForm(ModelForm):
    goodies = [
        'street',
        'city',
        'state',
        'zipCode',
        'country',
    ]

    class Meta:
        model = Home
        exclude = ('user', 'items', 'location')

    def get_loc_data(self):
        """Get fields related to a Home's location."""
        ret = {}
        for goodie in HomeForm.goodies:
            ret[goodie] = self.data[goodie]
        return ret

    def get_loc_data_as_string(self):
        return ', '.join(self.data[goodie] for goodie in HomeForm.goodies)  # in order of goodies


class ItemsForm(ModelForm):
    class Meta:
        model = Items
        exclude = ('user',)
