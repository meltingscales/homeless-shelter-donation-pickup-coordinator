import random

from django.contrib import admin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import *
from django.shortcuts import render, redirect

"""
An create+update view in a single class.
"""
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView


class BaseCreateOrUpdateView(ModelFormMixin, ProcessFormView):
    """
    Merging the logic of Django's
    :class:`~django.views.generic.edit.BaseCreateView` and
    :class:`~django.views.generic.edit.BaseUpdateView`

    Just like the the base views in Django, this class level
    don't have a ``render_to_response`` and only provide the workflow logic.
    """

    def _setup(self):
        if self.pk_url_kwarg in self.kwargs or self.slug_url_kwarg in self.kwargs:
            # Edit view
            self.object = self.get_object()
            self.is_add = False
        else:
            # Add view
            self.object = None
            self.is_add = True

    def get(self, request, *args, **kwargs):
        self._setup()
        return super(BaseCreateOrUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self._setup()
        return super(BaseCreateOrUpdateView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseCreateOrUpdateView, self).get_context_data(**kwargs)
        context['is_add'] = self.is_add
        return context


class CreateOrUpdateView(SingleObjectTemplateResponseMixin, BaseCreateOrUpdateView):
    """
    Merging the logic of Django's
    :class:`~django.views.generic.edit.CreateView` and
    :class:`~django.views.generic.edit.UpdateView`

    This provides the class to inherit from for standard views.
    """
    template_name_suffix = '_form'


# Create your views here.

def index(request: HttpRequest):
    context = {
        "test": [random.randrange(1, 101, 1) for _ in range(10)]
    }

    return render(request, 'index.html', context)


def signup(request: HttpRequest):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('root')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def profile(request: HttpRequest):
    template = 'donator/profile.html'

    return render(request, template)


def get_user_profile(request: HttpRequest, username: str):
    user = admin
