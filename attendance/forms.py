from django import forms
from django.contrib.auth.models import User

from attendance.models import Class, Teacher, Student


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(max_length=50)


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['grade', 'division']


class UserAddForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    email = forms.EmailField()


class TeacherAddForm(UserAddForm):
    which_class = forms.ModelChoiceField(queryset=Class.objects.all())


class TeacherRemoveForm(forms.Form):
    teacher = forms.ModelChoiceField(queryset=(Teacher.objects.all()))


class StudentAddForm(UserAddForm):
    phone = forms.IntegerField(max_value=9999999999)


class InorrectParameterException(Exception):
    pass


def get_StudentRemoveForm(query_set, POST):
    class StudentRemoveForm(forms.Form):
        student = forms.ModelChoiceField(queryset=query_set)

    if POST is None:
        return StudentRemoveForm()
    else:
        return StudentRemoveForm(POST)
