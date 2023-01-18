from django.db import models

# Create your models here.

class File(models.Model):
    CHOICES_FT = (('F', 'File'), ('U', 'URL'))

    Order = models.IntegerField(default=0, blank=True, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    page = models.CharField(max_length=100, null=True, blank=True)
    filetype = models.CharField(max_length=1, choices=CHOICES_FT, default='L')
    file = models.FileField(upload_to='static/files/', null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True, default='')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'page']


class Page(models.Model):
    CHOICES_PT = (('M', 'Main'), ('C', 'Child'))
    name = models.CharField(max_length=120, null=True, blank=True)
    title = models.CharField(max_length=120, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    page_type = models.CharField(max_length=1, null=True, blank=True, default='C')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class SystemInfo(models.Model):
    setting_name = models.CharField(max_length=50, null=True, blank=True)
    setting_text = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.setting_name + ' = ' + self.setting_text

    class Meta:
        ordering = ['setting_name']


class Sys_Settings:
    orgname = ""
    supportlink = ""

    # create constructor and initialize variables
    def __init__(self):
        self.orgname = self.get_orgname()
        self.supportlink = self.get_supportlink()

    # load orgname from SystemInfo
    def get_orgname(self):
        orgname = ''
        try:
            orgname = SystemInfo.objects.get(setting_name='orgname').setting_text
        except:
            pass
        return orgname

    # load supportlink from SystemInfo
    def get_supportlink(self):
        supportlink = ''
        try:
            supportlink = SystemInfo.objects.get(setting_name='supportlink').setting_text
        except:
            pass
        return supportlink
