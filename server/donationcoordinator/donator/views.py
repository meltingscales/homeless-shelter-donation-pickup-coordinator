from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import *
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.db import models

from .forms import *


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


def my_homes(request):
    """A User wants a list of their Homes."""
    template_name = "donator/home_list.html"
    context = {}
    user: User = request.user

    print("does " + str(user.username) + " want their homes?!")

    homes = Home.objects.filter(user=user)

    print("List of homes:")
    print(homes)

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


class HomeDetail(DetailView):
    model = Home
    template_name = 'donator/home_detail.html'

    def get_context_data(self, **kwargs):
        context = super(HomeDetail, self).get_context_data(**kwargs)
        return context


def home_detail(request):
    """A User wants details about one of their Homes."""
    return HttpResponse("home details???")

class HomeDelete(DeleteView):
    model = Home
    template_name = 'donator/home_delete.html'

    def get_success_url(self):
        return reverse('donator:home_list')
