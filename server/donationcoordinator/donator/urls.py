"""donator URL Configuration

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
from django.conf.urls import url
from django.urls import path
from django.views.generic import UpdateView, DeleteView

from . import views
from .forms import HomeForm
from .models import Home
from .views import HomeCreate, HomeDetail, HomeDelete

app_name = 'donator'

urlpatterns = [

    url(r'^$', views.index),

    # List person's Homes
    path(r'my-homes/', views.my_homes, name="home_list"),

    # Detail of one Home
    path(r'my-homes/<int:pk>/',
         HomeDetail.as_view(),
         name="home_detail",
         ),

    # Create a new Home
    path(r'my-homes/new/',
         HomeCreate.as_view(),
         name="home_create",
         ),

    # Edit home details, ex.: /donator/my-homes/1/edit/
    path(r'my-homes/<int:pk>/edit/',
         UpdateView.as_view(
             model=Home,
             template_name='donator/form.html',
             form_class=HomeForm),
         name="home_edit",
         ),

    # delete home by ID, ex.: /donator/my-homes/1/delete/
    path(r'my-homes/<int:pk>/delete/',
         HomeDelete.as_view(),
         name="home_delete",
         )
]
