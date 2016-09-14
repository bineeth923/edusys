from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from attendance.forms import LoginForm, ClassForm, TeacherAddForm, TeacherRemoveForm, StudentAddForm, \
    get_StudentRemoveForm
from attendance.models import Class, Teacher, Student
from helper import *


class UserIntegretyFailException(Exception):
    pass


def redirect_user_to_index(user):
    """
    Used to direct user to their corresponding index page
    :param user: User
    :return: HttpResponse
    """
    if is_student(user):
        # do something
        return HttpResponseRedirect(reverse('admin_index'))

    elif is_teacher(user):
        # do something
        return HttpResponseRedirect(reverse('teacher_index'))

    elif is_admin(user):
        # do something
        return HttpResponseRedirect(reverse('admin_index'))
    elif is_principal(user):
        # do something
        return HttpResponseRedirect(reverse('admin_index'))
    else:
        raise UserIntegretyFailException


def common_login(request):
    if request.user.is_authenticated():
        return redirect_user_to_index(request.user)
    context = get_error_context(request)
    context['form'] = LoginForm()
    return render(request, 'attendance/login.html', context)


def validate_login(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        return HttpResponseRedirect(reverse('login') + '?status=error')
    user = authenticate(username=username, password=password)
    if user is None:
        return HttpResponseRedirect(reverse('login') + '?status=error')
    login(request, user)
    # the following is to classify the user
    return redirect_user_to_index(user)
    # No need for a default as user will be one of these, else the user creation system is flawed


########################################################################################################################
#                                             Admin Controller                                                         #
########################################################################################################################
@admin_login_required
def admin_index(request):
    context = get_error_context(request)
    return render(request, 'attendance/admin_index.html', context)


@admin_login_required
def admin_teacher_add(request):
    if request.method == 'POST':
        form = TeacherAddForm(request.POST)
        if form.is_valid():
            try:
                user = User(username=form.cleaned_data['username'])
                user.email = form.cleaned_data['email']
                user.set_password(form.cleaned_data['password'])
                user.save()
                teacher = Teacher()
                teacher.set_user(user)
                teacher.which_class = form.cleaned_data['which_class']
                teacher.save()
            except IntegrityError:
                user = User.objects.get(username=form.cleaned_data['username'])
                if is_teacher(user):
                    user.set_password(form.cleaned_data['password'])
                    user.email = form.cleaned_data['email']
                    user.save()
                else:
                    return HttpResponseRedirect(reverse('admin_teacher_add') + "?status=error")
            return HttpResponseRedirect(reverse('admin_teacher_add') + "?status=success")
        else:
            return HttpResponseRedirect(reverse('admin_teacher_add') + "?status=error")
    else:
        context = get_error_context(request)
        form = TeacherAddForm()
        context['form'] = form
        return render(request, 'attendance/admin_teacher_add.html', context)


@admin_login_required
def admin_teacher_remove(request):
    if request.method == 'POST':
        form = TeacherRemoveForm(request.POST)
        if form.is_valid():
            try:
                teacher = form.cleaned_data['teacher']
                user = teacher.user
                user.delete()
                teacher.delete()
            except IntegrityError:
                return HttpResponseRedirect(reverse('admin_teacher_delete') + "?status=error")
            return HttpResponseRedirect(reverse('admin_teacher_delete') + "?status=success")
        else:
            return HttpResponseRedirect(reverse('admin_teacher_delete') + "?status=error")
    else:
        context = get_error_context(request)
        form = TeacherRemoveForm()
        context['form'] = form
        return render(request, 'attendance/admin_teacher_delete.html', context)


@admin_login_required
def admin_class_add(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except IntegrityError:
                return HttpResponseRedirect(reverse('admin_class_add') + "?status=error")
            return HttpResponseRedirect(reverse('admin_class_add') + "?status=success")
        return HttpResponseRedirect(reverse('admin_class_add') + "?status=error")
    else:
        context = get_error_context(request)
        form = ClassForm()
        context['form'] = form
        return render(request, 'attendance/admin_class_add.html', context)


########################################################################################################################
#                                           Teacher Controller                                                         #
########################################################################################################################

@teacher_login_required
def teacher_index(request):
    context = get_error_context(request)
    return render(request, 'attendance/teacher_index.html', context)


@teacher_login_required
def teacher_add_student(request):
    if request.method == 'POST':
        form = StudentAddForm(request.POST)
        if form.is_valid():
            try:
                user = User(username=form.cleaned_data['username'])
                user.email = form.cleaned_data['email']
                user.set_password(form.cleaned_data['password'])
                user.save()
                student = Student()
                student.set_user(user)
                student.phone = form.cleaned_data['phone']
                student.which_class = Class.objects.get(teacher__user=request.user)
                student.save()
            except IntegrityError:
                user = User.objects.get(username=form.cleaned_data['username'])
                user.email = form.cleaned_data['email']
                user.set_password(form.cleaned_data['password'])
                user.save()
                student = Student.objects.get(user=user)
                student.phone = form.cleaned_data['phone']
                student.save()
            return HttpResponseRedirect(reverse('teacher_student_add') + "?status=success")
        else:
            return HttpResponseRedirect(reverse('teacher_student_add') + "?status=error")
    else:
        context = get_error_context(request)
        form = StudentAddForm()
        context['form'] = form
        return render(request, 'attendance/teacher_student_add.html', context)


@teacher_login_required
def teacher_remove_student(request):
    teacher = Teacher.objects.get(user=request.user)
    query_set = Student.objects.filter(which_class=teacher.which_class)

    if request.method == 'POST':
        form = get_StudentRemoveForm(query_set, request.POST)
        if form.is_valid():
            try:
                student = form.cleaned_data['student']
                student.user.delete()
                student.delete()
            except IntegrityError:
                return HttpResponseRedirect(reverse('teacher_student_remove') + "?status=error")
            return HttpResponseRedirect(reverse('teacher_student_remove') + "?status=success")
        else:
            return HttpResponseRedirect(reverse('teacher_student_remove') + "?status=error")
    else:
        context = get_error_context(request)

        form = get_StudentRemoveForm(query_set, None)
        context['form'] = form
        return render(request, 'attendance/teacher_student_delete.html', context)
