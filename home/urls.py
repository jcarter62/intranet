from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),
    path('home/', views.home),
    path('home/<str:page>/', views.homewithpage),
    path('about/', views.about),
]
