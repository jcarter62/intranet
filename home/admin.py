from django.contrib import admin
from . import models
from import_export.admin import ImportExportModelAdmin


# @admin.register(models.File)
class FileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display_links = ('name',)
    list_display = ['Order', 'name', 'page', 'filetype', 'file', 'url']
    list_editable = ['Order', 'page', 'filetype', 'file', 'url']
    search_fields = ['name', 'page']
    list_per_page = 10
    list_filter = ['page']
    # ref: https://stackoverflow.com/a/180816
    save_as = True


admin.site.register(models.File, FileAdmin)


# @admin.register(models.Page)
class PageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display_links = ('name',)
    list_display = ['name', 'title', 'description', 'page_type']
    list_editable = ['title', 'description', 'page_type']
    search_fields = ['name']
    list_per_page = 10
    # ref: https://stackoverflow.com/a/180816
    save_as = True



admin.site.register(models.Page, PageAdmin)


class SystemInfoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display_links = ('setting_name',)
    list_display = ['setting_name', 'setting_text']
    # list_editable = ['setting_name', 'setting_text']
    search_fields = ['setting_name']
    list_per_page = 10


admin.site.register(models.SystemInfo, SystemInfoAdmin)


class SessionInfoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display_links = ('session_id',)
    list_display = ['record_id', 'session_id', 'key_name', 'key_text', 'created', 'updated']
    list_editable = ['key_name', 'key_text']
    search_fields = ['session_id', 'key_name']
    list_per_page = 10


admin.site.register(models.SessionInfo, SessionInfoAdmin)

