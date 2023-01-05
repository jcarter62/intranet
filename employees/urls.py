from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.employees_all),
    path('<str:id>', views.employee)
]
