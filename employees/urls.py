from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.employees_all_exclude_expired, name='employees'),
    path('all', views.employees_all_show_expired, name='employees_all'),
    path('<str:id>', views.employee, name='employee'),
    path('edit/<str:id>', views.employee_edit, name='employee_edit'),
    path('edit/image/<str:id>', views.employee_edit_image, name='employee_edit_image'),
]
