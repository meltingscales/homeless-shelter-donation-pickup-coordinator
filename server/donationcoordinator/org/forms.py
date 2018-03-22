from django.forms import ModelForm

from .models import Org


class OrgForm(ModelForm):
    class Meta:
        model = Org
        exclude = ()
