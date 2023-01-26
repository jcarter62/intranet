from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='root'),
    path('home/', views.home, name='home'),
    path('home/<str:page_name>/', views.homewithpage),
    path('about/', views.about, ),
    path('favicon.ico', views.favicon),
]
