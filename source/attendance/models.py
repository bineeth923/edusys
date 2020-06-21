from __future__ import unicode_literals

from django.contrib.auth.models import User, Group
from django.db import models


# Create your models here.

class Class(models.Model):
    grade = models.CharField(max_length=20)
    division = models.CharField(max_length=20, null=True)

    def __str__(self):
        return str(self.grade) + ":" + str(self.division)


class Subject(models.Model):
    name = models.CharField(max_length=200)
    classes = models.ManyToManyField(Class, related_name='subjects')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name) + ":" + str(self.id)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    which_class = models.ForeignKey(Class, null=True, default=None, on_delete=models.DO_NOTHING, related_name='teacher')
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def set_user(self, user):
        self.user = user
        self.user.groups.add(Group.objects.get(name='Teacher'))

    def remove(self):
        self.user.delete()
        self.delete()

    def __str__(self):
        return str(self.name) + ":" + str(self.id)


class TeacherSubjectAssociation(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subject_name = self.subject.name

    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING, related_name='teacher_subject_association')
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, related_name='teacher_subject_association')

    class Meta:
        db_table = 'attendance_teacher_subject_association'


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
    which_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')
    phone = models.BigIntegerField()
    email = models.EmailField()
    roll_no = models.IntegerField(unique=False)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def set_user(self, user):
        self.user = user
        self.user.groups.add(Group.objects.get(name='Student'))

    def remove(self):
        self.user.delete()
        self.delete()

    def __str__(self):
        return self.name


class Parent(models.Model):
    student = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='parent')
    email = models.CharField(max_length=100)
    phone = models.IntegerField()
    name = models.CharField(max_length=100)


class Attendance(models.Model):
    date = models.DateTimeField(null=False)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING, null=False)
    teacher_subject_association = models.ForeignKey(TeacherSubjectAssociation, on_delete=models.CASCADE)
    hour = models.CharField(null=False, max_length=20)
    is_present = models.BooleanField(default=False)


class Test(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
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
