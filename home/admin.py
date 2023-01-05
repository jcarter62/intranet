from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.File)
class EmployeeAdmin(admin.ModelAdmin):
    list_display_links = ('name',)
    list_display = ['Order', 'name', 'page', 'filetype', 'file', 'url']
    list_editable = ['Order', 'page', 'filetype', 'file', 'url']
    search_fields = ['name', 'page']
    list_per_page = 10
