from rest_framework import serializers

from attendance.models import Teacher, Class, Subject, TeacherSubjectAssociation, Student


class TeacherSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )
    teacher_subject_association = serializers.SlugRelatedField(many=True,
                                                               read_only=True,
                                                               slug_field='subject_name')

    class Meta:
        model = Teacher
        fields = '__all__'


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
