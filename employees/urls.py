from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.employees_all, name='employees'),
    path('<str:id>', views.employee, name='employee'),
    path('edit/<str:id>', views.employee_edit, name='employee_edit'),
]
