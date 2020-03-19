"""django_notes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from notes import views
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from notes.models import Note
from rest_framework import routers

info_dict = {
    'queryset': Note.objects.all(),
    'date_field': 'pub_date',
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('note/', include('notes.urls')),
    path('', views.index, name='index'),
    path('signin/', views.sign_in),
    path('signup/', views.sign_up, name='signup'),
    path('user/', views.show_user),
    path('logout/', views.logout),
    path('sitemap.xml', sitemap, {'sitemaps': {'blog':GenericSitemap(info_dict, priority=0.6)}}, name='django.contrib.sitemaps.views.sitemap'),
]
