from django.contrib import admin

# Register your models here.
from attendance.models import Class, Attendance, Marks, Parent, Subject, Test, Student, Teacher


@admin.register(Class, Teacher, Student)
class ClassAdmin(admin.ModelAdmin):
    pass
