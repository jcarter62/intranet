from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone']
    list_editable = ['email', 'phone']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    list_per_page = 10
