from django.forms import ModelForm

from .models import Items, Home


class HomeForm(ModelForm):
    class Meta:
        model = Home
        exclude = ('user', 'items',)


class ItemsForm(ModelForm):
    class Meta:
        model = Items
        exclude = ('user',)
