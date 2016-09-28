from django.contrib import admin

# Register your models here.
from attendance.models import Class, Attendance, Marks, Parent, Subject, Test, Student, Teacher, Principal


@admin.register(Class, Teacher, Student, Principal, Subject, Test)
class ClassAdmin(admin.ModelAdmin):
    pass
