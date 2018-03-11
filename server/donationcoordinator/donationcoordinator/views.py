import random

from django.http import *
from django.shortcuts import render


# Create your views here.

def index(request: HttpRequest):
    context = {
        "test": [random.randrange(1, 101, 1) for _ in range(10)]
    }

    return render(request, 'index.html', context)
