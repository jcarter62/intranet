from django.forms import ModelForm
from django import forms
from .models import *

class SignupForm(ModelForm):

    class Meta:
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'password1']

    def __str__(self):
        return self.username