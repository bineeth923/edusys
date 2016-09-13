from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Parent(models.Model):
    student = models.ForeignKey(User)
    email = models.CharField(max_length=100)
    phone = models.IntegerField()
    name = models.CharField(max_length=100)


class Class(models.Model):
    grade = models.IntegerField()
    division = models.CharField(max_length=1)
    teacher = models.ManyToManyField(User)


class Attendance(models.Model):
    date = models.DateTimeField()
    which_class = models.ForeignKey(Class)
    student = models.ForeignKey(User)
    is_present = models.BooleanField(default=True)


class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User)
    which_class = models.ForeignKey(Class)


class Test(models.Model):
    subject = models.ForeignKey(Subject)
    total_marks = models.IntegerField()
    name = models.CharField(max_length=100)
    date = models.DateField()


class Marks(models.Model):
    marks = models.DecimalField(decimal_places=2, max_digits=7)
    test = models.ForeignKey(Test)
    student = models.ForeignKey(User)


# Experimental feature to be added
'''
class Remarks(models.Model):
    student = models.ForeignKey(User)
    teacher = models.ForeignKey(User)
    remark = models.TextField()
    date = models.DateField()
'''
