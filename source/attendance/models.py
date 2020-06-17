from __future__ import unicode_literals

from django.contrib.auth.models import User, Group
from django.db import models


# Create your models here.

class Class(models.Model):
    grade = models.CharField(max_length=20)
    division = models.CharField(max_length=20)

    def __str__(self):
        return str(self.grade) + ":" + str(self.division)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    which_class = models.ForeignKey(Class, null=True, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def set_user(self, user):
        self.user = user
        self.user.groups.add(Group.objects.get(name='Teacher'))

    def remove(self):
        self.user.delete()
        self.delete()

    def __str__(self):
        return str(self.name) + "-" + str(self.which_class)


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def set_user(self, user):
        self.user = user
        self.user.groups.add(Group.objects.get(name='Admin'))

    def remove(self):
        self.user.delete()
        self.delete()

    def __str__(self):
        return str(self.name)


class Principal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def set_user(self, user):
        self.user = user
        self.user.groups.add(Group.objects.get(name='Principal'))

    def remove(self):
        self.user.delete()
        self.delete()

    def __str__(self):
        return str(self.name)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    which_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    phone = models.BigIntegerField()
    roll_no = models.IntegerField(unique=False)
    name = models.CharField(max_length=100)

    def set_user(self, user):
        self.user = user
        self.user.groups.add(Group.objects.get(name='Student'))

    def remove(self):
        self.user.delete()
        self.delete()

    def __str__(self):
        return self.name


class Parent(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=100)
    phone = models.IntegerField()
    name = models.CharField(max_length=100)


class Attendance(models.Model):
    date = models.DateTimeField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_present = models.BooleanField(default=True)


class Subject(models.Model):
    name = models.CharField(max_length=100)
    which_class = models.ForeignKey(Class, on_delete=models.CASCADE)


class Test(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    total_marks = models.IntegerField()
    name = models.CharField(max_length=100, unique=False)
    date = models.DateField()


class Marks(models.Model):
    marks = models.DecimalField(decimal_places=2, max_digits=7)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)


# Experimental feature to be added
'''
class Remarks(models.Model):
    student = models.ForeignKey(User)
    teacher = models.ForeignKey(User)
    remark = models.TextField()
    date = models.DateField()
'''
