from django.contrib.auth.models import User
from rest_framework import serializers

from attendance.models import Teacher, Class, Subject, TeacherSubjectAssociation, Student, Attendance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'
        depth = 1


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class TeacherSubjectAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSubjectAssociation
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    which_class = ClassSerializer()

    class Meta:
        model = Student
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class MarkAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['phone', 'email', 'roll_no', 'name']
