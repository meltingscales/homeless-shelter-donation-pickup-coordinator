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
from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views
from .views import HomeDetail, HomeDelete, HomeCreateOrUpdate, ItemsUpdate, HomeCreate

app_name = 'donator'

urlpatterns = [

    # User's profile
    path(r'', views.view_profile, name="profile_view"),

    # Update user's profile
    path(r'my-profile/update/', views.update_profile, name="profile_update"),

    # Export data
    path(r'export/', views.export_data, name='export_data'),

    # List person's Homes
    path(r'my-homes/', login_required(views.my_homes), name="home_list"),

    # Detail of one Home
    path(r'my-homes/<int:pk>/',
         login_required(
             HomeDetail.as_view()
         ),
         name="home_detail",
         ),

    path(r'my-homes/<int:pk>/update-items/',
         login_required(
             ItemsUpdate.as_view()
         ),
         name="items_update",
         ),

    # Create a new Home
    path(r'my-homes/new/',
         login_required(
             HomeCreate.as_view()
         ),
         name="home_create",
         ),

    # Edit home details, ex.: /donator/my-homes/1/edit/
    path(r'my-homes/<int:pk>/edit/',
         login_required(
             HomeCreateOrUpdate.as_view()
         ),
         name="home_edit",
         ),

    # delete home by ID, ex.: /donator/my-homes/1/delete/
    path(r'my-homes/<int:pk>/delete/',
         login_required(
             HomeDelete.as_view()
         ),
         name="home_delete",
         )
]
