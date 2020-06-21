from django.contrib.auth.models import User
from django.core import serializers
from django.db import IntegrityError
from rest_framework import generics, mixins, status
from rest_framework.response import Response

from attendance.api.serializer import TeacherSerializer, ClassSerializer
from attendance.models import Teacher, Class


def create_user(username, password):
    user = User(username=username)
    user.set_password(password)
    user.save()
    return user


class Helpers:
    pass


class TeacherAPI(mixins.ListModelMixin,
                 mixins.UpdateModelMixin,
                 generics.GenericAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

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

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ClassAPI(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               mixins.UpdateModelMixin,
               generics.GenericAPIView):
    queryset = Class.objects.filter(teacher__isnull=True)
    serializer_class = ClassSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
