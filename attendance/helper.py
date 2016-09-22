"""
Author : Sidhin S Thomas

Any enquiries regarding code, email at sidhin.thomas@gmail.com

Copyright 2016 Shift2Cloud Technologies
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

"""
These functions are to check is a giving User is of which type
"""


def is_teacher(user):
    return user.groups.filter(name='Teacher').exists()


def is_student(user):
    return user.groups.filter(name='Student').exists()


def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def is_principal(user):
    return user.groups.filter(name='Principal').exists()


"""
View helper function to generate a context for the template in case error message is to be printed
"""


def get_error_context(request):
    try: # TODO set appropriate error codes
        error = request.GET['status']
        context = {'error_message': 'Something went wrong'}
    except KeyError:
        context = {}
    return context


########################################################
#                   Decorators                         #
########################################################

"""
These decorators help to make sure that only a particular user group is allowed access
"""


def admin_login_required(function):
    def wrapper(request):
        if not is_admin(request.user):
            return render(request, 'attendance/unauthorised.html')
        return function(request)

    return wrapper


def teacher_login_required(function):
    def wrapper(request):
        if not is_teacher(request.user):
            return render(request, 'attendance/unauthorised.html')
        return function(request)

    return wrapper


def principal_login_required(function):
    def wrapper(request):
        if not is_principal(request.user):
            return render(request, 'attendance/unauthorised.html')
        return function(request)

    return wrapper


def student_login_required(function):
    def wrapper(request):
        if not is_student(request.user):
            return render(request, 'attendance/unauthorised.html')
        return function(request)

    return wrapper
