from django.http import *

from django.shortcuts import render


# Create your views here.
def index(request: HttpRequest):
    template_name = 'org/index.html'
    context = {}
    return render(request, template_name, context)


def new_org(request: HttpRequest):
    return HttpResponse("want to sign up as an org??")


def org_list(request: HttpRequest):
    return HttpResponse("list o' orgs anyone?")
