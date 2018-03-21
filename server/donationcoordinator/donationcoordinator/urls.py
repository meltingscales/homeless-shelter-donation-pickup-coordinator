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
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

import donator.urls
import org.urls
import restaurantapp.urls
from . import views as core_views

app_name = "donationcoordinator"

urlpatterns = [
    path('', core_views.index, name='root'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', core_views.profile, name='profile'),
    path('accounts/signup/', core_views.signup, name='signup'),
    path('donator/', include(donator.urls, namespace='donator'), name='donator'),
    path('org/', include(org.urls, namespace='org'), name='org'),
    path('restaurantapp/', include(restaurantapp.urls, namespace='restaurantapp'), name='restaurantapp')
]
