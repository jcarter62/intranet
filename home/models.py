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

