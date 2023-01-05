from django.db import models


class Employee(models.Model):
    emp_id = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=120)
    start_date = models.CharField(max_length=50, null=True, blank=True)
    end_date = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    notes = models.TextField()
    department = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['last_name', 'first_name']

