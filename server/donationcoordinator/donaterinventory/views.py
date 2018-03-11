from django.shortcuts import render
from django.http import *

# Create your views here.

def index(request: HttpRequest):
    return HttpResponse("hi u wana donate??")