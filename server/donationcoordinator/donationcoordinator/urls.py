"""donationcoordinator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
import traceback

import django.contrib.auth.urls
from django import db
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

import donator.urls
import org.urls
from donator.models import User, HomeLocation
from org.models import Org
from . import views as core_views
from .startup import Startup

app_name = "donationcoordinator"

urlpatterns = [
    path('', core_views.index, name='index'),
    path('admin/', admin.site.urls),
    path('accounts/', include(django.contrib.auth.urls)),
    path('accounts/signup/', core_views.signup, name='signup'),
    path('donator/', include(donator.urls, namespace='donator'), name='donator'),
    path('org/', include(org.urls, namespace='org'), name='org'),
]

if 'STARTUP_DATABASE_TASKS' in os.environ and os.environ['STARTUP_DATABASE_TASKS'].lower() == 'true':

    print("Resetting database and populating it with default models!")

    try:
        Startup.delete_all_objects(Org, User, HomeLocation)

        Startup.create_test_users()

        db.connections.close_all()
    except Exception as e:
        print("Couldn't do startup tasks:")
        print(e)
        traceback.print_exc()
