from django.contrib import admin

# Register your models here.
from attendance.models import Class, Attendance, Marks, Parent, Subject, Test

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    pass