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


class UserAddForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class TeacherRemoveForm(forms.Form):
    teacher = forms.ModelChoiceField(queryset=User.objects.all().filter(groups__name='Teacher'))
