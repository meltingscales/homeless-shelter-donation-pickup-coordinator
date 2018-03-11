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
from django.utils import timezone
from django.views.generic import DetailView, ListView, UpdateView

from . import views
from .forms import RestaurantForm, DishForm
from .models import Restaurant, Dish
from .views import RestaurantCreate, DishCreate, RestaurantDetail

app_name = 'donator'

urlpatterns = [

    url(r'^$', views.index),

    # List latest 5 restaurants: /donator/
    url(r'restaurants/$',
        ListView.as_view(
            queryset=Restaurant.objects.filter(date__lte=timezone.now()).order_by('date')[:5],
            context_object_name='latest_restaurant_list',
            template_name='donator/restaurant_list.html'),
        name='restaurant_list'),

    # Restaurant details, ex.: /donator/restaurants/1/
    url(r'restaurants/(?P<pk>\d+)/\$',
        RestaurantDetail.as_view(),
        name='restaurant_detail'),

    # Restaurant dish details, ex: /donator/restaurants/1/dishes/1/
    url(r'restaurants/(?P<pkr>\d+)/dishes/(?P<pk>\d+)/',
        DetailView.as_view(
            model=Dish,
            template_name='donator/dish_detail.html'),
        name='dish_detail'),

    # Create a restaurant, /donator/restaurants/create/
    url(r'restaurants/create/',
        RestaurantCreate.as_view(success_url='cOOLBRO'),
        name='restaurant_create'),

    # Edit restaurant details, ex.: /donator/restaurants/1/edit/
    url(r'restaurants/(?P<pk>\d+)/edit/',
        UpdateView.as_view(
            model=Restaurant,
            template_name='donator/form.html',
            form_class=RestaurantForm),
        name='restaurant_edit'),

    # Create a restaurant dish, ex.: /donator/restaurants/1/dishes/create/
    url(r'restaurants/(?P<pk>\\d+)/dishes/create/',
        DishCreate.as_view(),
        name='dish_create'),

    # Edit restaurant dish details, ex.: /donator/restaurants/1/dishes/1/edit/
    url(r'restaurants/(?P<pkr>\\d+)/dishes/(?P<pk>\\d+)/edit/',
        UpdateView.as_view(
            model=Dish,
            template_name='donator/form.html',
            form_class=DishForm),
        name='dish_edit'),

    # # Create a restaurant review, ex.: /donator/restaurants/1/reviews/create/
    # # Unlike the previous patterns, this one is implemented using a method view instead of a class view
    # url(r'\^restaurants/(?P<pk>\\d+)/reviews/create/\$',
    #     'donator.views.review',
    #     name='review_create'),
    #
]
