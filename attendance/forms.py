from django import forms
from django.contrib.auth.models import User

from attendance.models import Class


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(max_length=50)


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['grade', 'division', 'teacher']
