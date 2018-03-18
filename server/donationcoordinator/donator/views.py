from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from django.http import *
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import *
from .models import User


# Create your views here.


def index(request: HttpRequest):
    template_name = 'donator/index.html'
    context = {}
    return render(request, template_name, context)


def signup(request):
    template_name = 'registration/signup.html'

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, template_name, {'form': form})


def my_homes(request, context={}):
    """A User wants a list of their Homes."""
    template_name = "donator/home_list.html"
    user: User = request.user

    homes = Home.objects.filter(user=user)

    context["homes_list"] = homes

    return render(request, template_name, context)


class HomeCreate(CreateView):
    model = Home
    template_name = 'donator/form.html'
    # success_url = reverse_lazy('restaurant_detail')
    form_class = HomeForm

    def get_success_url(self):
        return reverse('donator:home_detail', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(HomeCreate, self).form_valid(form)


class HomeUpdate(UpdateView):
    model = Home
    template_name = 'donator/form.html'
    form_class = HomeForm

    def get_object(self, queryset=None) -> Home:
        """ Hook to ensure object is owned by request.user. """

        obj = super(HomeUpdate, self).get_object()
        if not obj.user == self.request.user:
            raise PermissionDenied
        return obj


class HomeDetail(DetailView):
    model = Home
    template_name = 'donator/home_detail.html'

    def get_object(self, queryset=None) -> Home:
        """ Hook to ensure object is owned by request.user. """

        obj = super(HomeDetail, self).get_object()
        if not obj.user == self.request.user:
            raise PermissionDenied
        return obj

    def get_context_data(self, **kwargs):
        context = super(HomeDetail, self).get_context_data(**kwargs)
        return context


class HomeDelete(DeleteView):
    model = Home
    template_name = 'donator/home_delete.html'

    def get_object(self, queryset=None) -> Home:
        """ Hook to ensure object is owned by request.user. """

        obj = super(HomeDelete, self).get_object()
        if not obj.user == self.request.user:
            raise PermissionDenied
        return obj

    def get_success_url(self):
        return reverse('donator:home_list')

    def form_valid(self, request: HttpRequest):

        if 'home_name' not in request.POST:
            return False

        form_name = request.POST['home_name']
        home_name = self.get_object().name

        return form_name == home_name  # make sure they type the name to confirm

    def post(self, request: HttpRequest, *args, **kwargs):

        if self.form_valid(request):
            print("Form is valid for delete!")
            self.get_object().delete()
            return HttpResponseRedirect(self.get_success_url())
        else:  # they can't delete
            context = {
                'error_message': 'Cannot delete! You must type in the home\'s name to confirm!',
                'home': self.get_object(),
            }

            return render(request, self.template_name, context)
