import random

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import *
from django.shortcuts import render, redirect
from django.contrib import admin



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

    print(f"'{request.user}' asked for their profile.")

    return render(request, 'registration/profile.html')

def get_user_profile(request: HttpRequest, username: str):
    user = admin