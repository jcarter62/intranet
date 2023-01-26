from django.forms import ModelForm
from django import forms
from .models import Employee as em


class EmployeeEditForm(ModelForm):
    class Meta:
        model = em
        fields = ['first_name', 'last_name', 'position', 'department',
                  'start_date', 'end_date', 'email', 'phone', 'notes']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'date'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }
