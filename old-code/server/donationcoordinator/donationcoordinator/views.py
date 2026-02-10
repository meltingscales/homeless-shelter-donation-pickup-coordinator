from django.contrib.auth import login, authenticate
from django.http import *
from django.shortcuts import render, redirect
from django.views.generic import ListView

from donator.forms import UserCreationForm

"""
An create+update view in a single class.
"""
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView, FormMixin


class FormListView(FormMixin, ListView):
    # from https://stackoverflow.com/questions/6406553/django-class-based-view-listview-with-form
    def get(self, request, *args, **kwargs):
        # From ProcessFormMixin
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)

        # From BaseListView
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})

        context = self.get_context_data(object_list=self.object_list, form=self.form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


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

    def get_object(self, queryset=None):
        try:
            return super(CreateOrUpdateView, self).get_object(queryset)
        except AttributeError:
            return None


# Create your views here.

def index(request: HttpRequest):
    context = {}

    return render(request, 'index.html', context)


def signup(request: HttpRequest):
    template = 'registration/signup.html'

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, template, {'form': form})


def profile(request: HttpRequest):
    template = 'donator/profile.html'

    return render(request, template)
