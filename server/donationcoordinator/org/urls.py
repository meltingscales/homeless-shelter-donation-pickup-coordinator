"""org URL Configuration

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
from django.urls import path

from . import views
from .views import OrgDetail, OrgCreateOrUpdate, OrgCreate

app_name = 'org'
urlpatterns = [
    # view own org
    path(r'',
         views.my_org,
         name='index'
         ),

    # create new org
    path(r'new/',
         OrgCreate.as_view(),
         name='new_org'
         ),

    # edit own org
    path(r'orgs/<int:pk>/edit',
         OrgCreateOrUpdate.as_view(),
         name='org_edit',
         ),

    # list of orgs
    path(r'orgs/', views.org_list, name='org_list'),

    # view other org
    path(r'orgs/<int:pk>/',
         OrgDetail.as_view(),
         name='org_detail',
         ),

]
