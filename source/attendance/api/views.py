from django.contrib.auth.models import User
from django.core import serializers
from django.db import IntegrityError, transaction
from rest_framework import generics, mixins, status, permissions
from rest_framework.response import Response

from attendance.api.serializer import TeacherSerializer, ClassSerializer, SubjectSerializer, \
    TeacherSubjectAssociationSerializer, StudentSerializer, MarkAttendanceSerializer
from attendance.error import ClassNotFoundException, StudentNotFoundException
from attendance.helper import is_student, is_teacher
from attendance.models import Teacher, Class, Subject, TeacherSubjectAssociation, Student, Attendance


def create_user(username, password):
    user = User(username=username)
    user.set_password(password)
    user.save()
    return user


class Helpers:
    pass


class Base(mixins.ListModelMixin,
           mixins.UpdateModelMixin,
           mixins.CreateModelMixin,
           mixins.RetrieveModelMixin,
           mixins.DestroyModelMixin,
           generics.GenericAPIView):
    lookup_field = 'id'
    permission_classes = [permissions.DjangoObjectPermissions]

    def get(self, request, *args, **kwargs):
        if not kwargs:
            return self.list(request, *args, **kwargs)
        else:
            return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TeacherAPI(Base):
    serializer_class = TeacherSerializer

    def get_queryset(self):
        """
        If a specific user group logs in, the queryset will be filtered according to that.
        Else, returning all the objects. Further permission is at the django permission checks
        :return:
        """
        if is_teacher(self.request.user):
            return Teacher.objects.filter(user=self.request.user)
        return Teacher.objects.all()

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            user = create_user(request.data['user_id'], request.data['password'])
            # TODO: Not considering which_class component currently.
            teacher = Teacher()
            teacher.set_user(user)
            teacher.name = request.data['name']
            teacher.save()
        except IntegrityError:
            return Response(data={"error: IntegrityError"}, status=status.HTTP_409_CONFLICT)
        return Response(data=serializers.serialize('json', [teacher]), status=status.HTTP_201_CREATED)


class ClassAPI(Base):
    serializer_class = ClassSerializer

    def get_queryset(self):
        """
        If a specific user group logs in, the queryset will be filtered according to that.
        Else, returning all the objects. Further permission is at the django permission checks
        :return:
        """
        if is_student(self.request.user):
            return Class.objects.filter(students__user=self.request.user)
        elif is_teacher(self.request.user):
            return Class.objects.filter(teacher__user=self.request.user). \
                union(Class.objects.filter(subjects__classes__teacher__user=self.request.user))
        return Class.objects.all()


class SubjectAPI(Base):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class TeacherSubjectAPI(Base):
    queryset = TeacherSubjectAssociation.objects.all()
    serializer_class = TeacherSubjectAssociationSerializer


class StudentAPI(Base):
    serializer_class = StudentSerializer

    def get_queryset(self):
        """
        If a specific user group logs in, the queryset will be filtered according to that.
        Else, returning all the objects. Further permission is at the django permission checks
        :return:
        """
        if is_student(self.request.user):
            return Student.objects.filter(user=self.request.user)
        return Student.objects.all()

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            # TODO: Cleanup Auth user obj if failed.
            user = create_user(request.data.pop('user_id'), request.data.pop('password'))
            class_obj = Class.objects.get(pk=request.data.pop('which_class'))
            if not class_obj:
                raise ClassNotFoundException
            student = Student(**request.data)
            student.set_user(user)
            student.which_class = class_obj
            student.save()
        except IntegrityError as err:
            return Response(data={"error": "IntegrityError", "msg": err.__str__()}, status=status.HTTP_409_CONFLICT)
        except KeyError:
            return Response(data={"error": "KeyError", "msg": "mandatory key missing"},
                            status=status.HTTP_400_BAD_REQUEST)
        except ClassNotFoundException:
            return Response(data={"error": "ClassNotFoundException"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response(data=serializers.serialize('json', [student]), status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        try:
            # TODO: Currently supports to edit phone, email, roll_no, name
            instance = self.get_object()
            instance.phone = request.data['phone']
            instance.email = request.data['email']
            instance.roll_no = request.data['roll_no']
            instance.name = request.data['name']
            instance.save()
            return Response(data=serializers.serialize('json', [instance]), status=status.HTTP_202_ACCEPTED)
        except IntegrityError as err:
            return Response(data={"error": "IntegrityError", "msg": err.__str__()}, status=status.HTTP_409_CONFLICT)


class AttendanceAPI(Base):
    queryset = Attendance.objects.all()
    serializer_class = MarkAttendanceSerializer()

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if 'student' in request.data:
            # Admin/ Someone with a higher permission than Student's one
            try:
                serializer['student'] = Student.objects.get(id=request.pop('student'))
            except (KeyError or StudentNotFoundException) as err:
                return Response({"Errored": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # A student is trying to mark attendance
            pass

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
