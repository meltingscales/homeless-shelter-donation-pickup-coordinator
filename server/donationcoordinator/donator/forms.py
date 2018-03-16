from django.forms import ModelForm
from .models import User, Items, Home


class HomeForm(ModelForm):
    class Meta:
        model = Home
        exclude = ('user','items','image')


class ItemsForm(ModelForm):
    class Meta:
        model = Items
        exclude = ('user',)
