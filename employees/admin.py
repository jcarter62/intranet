from django.contrib import admin
from . import models
from import_export.admin import ImportExportModelAdmin


class EmployeeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone']
    list_editable = ['email', 'phone']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    list_per_page = 10
    list_filter = ['department']
    # ref: https://stackoverflow.com/a/180816
    save_as = True


admin.site.register(models.Employee, EmployeeAdmin)
