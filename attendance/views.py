from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseRedirect

# Create your views here.
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_date

from attendance.forms import LoginForm, ClassForm, TeacherAddForm, TeacherRemoveForm, StudentAddForm, \
    get_StudentRemoveForm
from attendance.models import Class, Teacher, Student, Subject
from attendance.helper import *


class UserIntegrityFailException(Exception):
    pass


class RollNoExistsError(Exception):
    pass


def redirect_user_to_index(user):
    """
    Used to direct user to their corresponding index page
    :param user: User
    :return: HttpResponseRedirect
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
        raise UserIntegrityFailException


def common_login(request):
    if request.user.is_authenticated():
        return redirect_user_to_index(request.user)
    context = get_error_context(request)
    context['form'] = LoginForm()
    return render(request, 'attendance/login.html', context)


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse('login'))


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


@admin_login_required
def admin_class_remove(request):
    if request.method == "POST":
        class_id = int(request.POST['class'])
        class_obj = Class.objects.get(pk=class_id)
        class_obj.delete()
        return HttpResponseRedirect(reverse('admin_class_remove') + '?status=success')
    else:
        '''
        Form :
        * select (class)
        '''
        context = get_error_context(request)
        class_list = Class.objects.all()
        context['class_list'] = class_list
        # TODO return(request, <template>, context)


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
                rol_list = [student.roll_no for student in
                            Student.objects.filter(which_class__teacher__user=request.user)]
                roll = form.cleaned_data['roll']
                if roll in rol_list:
                    raise RollNoExistsError
                user = User(username=form.cleaned_data['username'])
                user.email = form.cleaned_data['email']
                user.set_password(form.cleaned_data['password'])
                user.save()
                student = Student()
                student.set_user(user)
                student.phone = form.cleaned_data['phone']
                student.roll_no = form.cleaned_data['roll']
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
            except RollNoExistsError:
                return HttpResponseRedirect(reverse('teacher_student_add') + "?status=rollerror")
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


@teacher_login_required
def teacher_student_edit(request):
    student_list = Student.objects.filter(which_class__teacher__user=request.user)
    if request.method == "POST":
        '''
        Iterate student list and save details, after verifying roll_no
        '''
        roll_list = set()
        for student in student_list:
            string = 'student_' + str(student.id) + '_'
            roll = int(request.POST[string + 'roll'])
            if roll not in roll_list:
                roll_list.add(roll)
            else:
                return HttpResponseRedirect(reverse('teacher_student_edit') + "?=status=error")
        for student in student_list:
            string = 'student_' + str(student.id) + '_'
            student.roll_no = int(request.POST[string + 'roll'])
            student.phone = int(request.POST[string + 'phone'])
            which_class = Class.objects.get(pk=int(request.POST[string + 'class']))
            student.which_class = which_class
            student.save()
        return HttpResponseRedirect(reverse('teacher_student_edit') + "?status=success")
    else:
        '''
        Form :
        * list containing all students and textbox pre-filled with their details
        naming convention :
        * student_<id>_phone
        * student_<id>_roll
        * student_<id>_class
        redirect to same link
        '''
        context = get_error_context(request)
        class_list = Class.objects.all()
        context['class_list'] = class_list
        context['student_list'] = student_list
        return render(request, 'attendance/teacher_student_edit.html', context)


def teacher_subject_add(request):
    if request.method == "POST":
        subject = Subject()
        subject.name = request.POST['subject']
        subject.which_class = Teacher.objects.get(user=request.user).which_class
        subject.save()
        return HttpResponseRedirect(reverse('teacher_subject_add') + "?status=success")
    else:
        '''Form
        * Subject Name (subject)
        * Teacher Select (teacher)
        '''
        context = get_error_context(request)
        context['teacher_list'] = Teacher.objects.all()
        return render(request, 'attendance/teacher_subject_add.html', context)


def teacher_subject_edit(request):
    """
    To edit and delete subjects in class
    """
    context = get_error_context(request)
    subject_list = Subject.objects.filter(which_class__teacher__user=request.user)
    if request.method == "POST":
        for subject in subject_list:
            string = str(subject.id) + "_"
            if string + 'delete' in request.POST:
                subject.delete()
                continue
            subject.name = request.POST[string + 'name']
            subject.save()
        return HttpResponseRedirect(reverse('teacher_subject_edit')+"?=status=success")
    else:
        '''Form
        * List of all subjects
            * Subject name textbox
            * checkbox to delete it

            naming convention:
            <subject.id>_name
            <subject.id>_delete
        '''
        context['subject_list'] = subject_list
        return render(request, 'attendance/teacher_subject_edit.html', context)


@teacher_login_required
def teacher_test_add(request):
    student_list = Student.objects.filter(which_class__teacher__user=request.user)
    if request.method == "POST":
        ''' TASKs
            check if the object exists
             if no =>   after creating the Test object,
                        create Mark object for all students of the class
             if yes => Display a filled version of previous form to be edited

        '''
        # Do something
        try:
            date = request.POST['date']
            name = request.POST['test_name']
            total_marks = int(request.POST['marks_tot'])
            test_list = []
            for subject in Subject.objects.filter(which_class__teacher__user=request.user):
                test = Test()
                test.date = date
                test.name = name
                test.total_marks = total_marks
                test.subject = subject
                test.save()
                test_list.append(test)
            for test in test_list:
                for student in student_list:
                    string = str(test.subject.id) + '_' + str(student.roll_no)
                    marks = request.POST[string]
                    mark = Marks()
                    mark.student = student
                    mark.test = test
                    mark.marks = int(marks)
                    mark.save()
            return HttpResponseRedirect(reverse('teacher_test_add') + '?status=success')

        except KeyError:
            raise Exception("keyerr")
        except IntegrityError:
            raise Exception("Int")
        except TypeError:
            raise Exception("Type")
    else:
        '''Description of form required:
        * Test Name (test_name)
        * Marks out of (marks_tot)
        * Date (date)
        * for List of students
            > list of TextBox (<subject.id>_<student_roll>)
        '''
        teacher_list = Teacher.objects.all()
        subject_list = Subject.objects.filter(which_class__teacher__user=request.user)
        context = get_error_context(request)
        context['teacher_list'] = teacher_list
        context['subject_list'] = subject_list
        context['student_list'] = student_list
        return render(request, 'attendance/teacher_test_add.html', context)


@teacher_login_required
def teacher_test_edit(request):
    context = {}
    if request.method == "POST":
        test_name = request.POST['test']
        test_list = Test.objects.filter(name=test_name)
        if 'edit' in request.POST:
            """ When edit checkbox is selected"""
            '''FORM
            * textbox -> name : <mark.id>
            * total_marks -> name : total_mark
            '''
            test_list = test_list.order_by('name')
            mark_list = []
            for student in Student.objects.filter(which_class__teacher__user=request.user).order_by('roll_no'):
                marks = Marks.objects.filter(student=student, test__name=test_name).order_by('test__subject__name')
                mark_list.append(marks)
            context['test_list'] = test_list
            context['mark_list'] = mark_list
            '''
            -----Context details-----
            * mark_list -> a list of marks(list),
                            marks is a list of all mark objects of a student ordered by subject name.
            * test_list -> list of test objects
            '''
            return render(request, 'attendance/teacher_test_edit.html', context)
        elif 'delete' in request.POST:
            """
            When the delete checkbox is selected.
            """
            Test.objects.filter(name=test_name).delete()
        else:
            """ Editing the test, and marks associated with it"""
            total_mark = int(request.POST['total_mark'])
            for test in test_list:
                test.total_marks = total_mark
                test.save()
                marks = Marks.objects.filter(test=test)
                for mark in marks:
                    mark.marks = request.POST[str(mark.id)]
                    mark.save()
        return HttpResponseRedirect(reverse('teacher_test_select')+'?status=success')
    else:
        '''
        Form:
        * List of all exams:
        * list of test by name
        * 2 checkbox by name edit and delete
        '''
        test_names = [test.name for test in Test.objects.filter(subject__which_class__teacher__user=request.user)]
        test_names = set(test_names)
        context['test_names'] = test_names
        return render(request, 'attendance/teacher_test_select.html', context)


@teacher_login_required
def teacher_report_view_single(request):
    context = get_error_context(request)
    if request.method == "POST":
        '''Task
        * Get student from form
        * Get range of date
        return web page with required content
        '''
        student = Student.objects.get(pk=int(request.POST['subject']))
        from_date = parse_date(request.POST['from_date'])
        to_date = parse_date(request.POST['to_date'])
        attendance = get_attendance_report_from_to(student, from_date, to_date)
        mark_report_list = []
        for subject in Subject.objects.filter(which_class=student.which_class):
            test_list = mark_report_subject(student, subject)
            report = {'test_list': test_list, 'subject': subject}
            mark_report_list.append(report)
        context['student'] = student
        context['from_date'] = from_date
        context['to_date'] = to_date
        context['attendance'] = attendance
        context['mark_list'] = mark_report_list
        '''
        !--- Context details ---!
        * student
        * from_date
        * to_date
        * attendance :
            > Dictionary with keys : present, absent, total, percentage_present
        * mark_list list of dictionary
            with keys : test_list, subject
            > test_list : list of dictionary with keys : test_name,date,subject,marks,total_marks
            > subject
        '''
        # TODO return render(request,'<template>', context)
    else:
        '''Form Description
        * Student name
        * From date
        * To date
        '''
        context['student_list'] = Student.objects.filter(which_class__teacher__user=request.user)
        # TODO return render()


@teacher_login_required
def teacher_report_class(request):
    context = get_error_context(request)
    if request.method == "POST":
        '''Task
        * Get Subject List
        * Get From and To Date
        return table with the data
        '''
        subject = Subject.objects.get(pk=int(request.POST['subject']))
        student_list = Student.objects.filter(which_class__teacher__user=request.user)
        report_list = []
        for student in student_list:
            test_list = mark_report_subject(student, subject)
            attendance = get_attendance_complete(student)
            report = {'test_list': test_list, 'student': student, 'attendance': attendance}
            report_list.append(report)
        context['subject'] = subject
        context['report_list'] = report_list
        '''
        !--- Context details ---!
        * report_list :
            > list of reports:
            each report contains:
            * test_list in key 'test_list'
                the test_list is further a list of dictionaries.
                the keys in the dictionary are : test_name,date,subject,marks,total_marks
            * student in key 'student'
            * attendance in key 'attendance'
                Dictionary with keys: present, absent, total, percentage_present
        '''
        # TODO return render(request, '<template>', context)
    else:
        '''Form
        * Subject List (subject)
        '''
        context['subject_list'] = Subject.objects.filter(which_class__teacher__user=request.user)
        # TODO return render(request,'<template>', context)


@teacher_login_required
def teacher_attendance_today(request):
    teacher = Teacher.objects.get(user=request.user)
    student_list = Student.objects.filter(which_class=teacher.which_class)
    if request.method == "POST":
        '''Task
        Create attendance objects for each student
        and fill with data from form
        '''
        for student in student_list:
            string = 'student_' + str(student.id)
            is_present = string in request.POST
            attendance = Attendance(student=student)
            attendance.is_present = is_present
            attendance.date = timezone.now().date()
            attendance.save()
        # return redirect
        return HttpResponseRedirect(reverse('teacher_teacher_attendance_today'))
    else:
        ''' Task
        Check if attendance for today already taken,
            if taken => Show pre-filled attendance option and today's statistics
        else show the form :
        Form
        for each student in class
        * Student name as label, checkbox to determine present or not
        '''
        attendance = Attendance.objects.filter(student__which_class__teacher__user=request.user).filter(
            date=timezone.now().date()).order_by('student__roll_no')
        context = get_error_context(request)
        if attendance.count() != 0:
            present = 0
            absent = 0
            for a in attendance:
                if a.is_present:
                    present += 1
                else:
                    absent += 1
            percentage = float(present) / attendance.count() * 100
            context['absent'] = absent
            context['present'] = present
            context['total'] = attendance.count()
            percentage = "{0:.2f}".format(percentage)
            context['percentage'] = percentage
            return render(request, 'attendance/teacher_attendance_taken.html', context)
        context['student_list'] = student_list
        return render(request, 'attendance/teacher_attendance.html', context)
        # attendance, student_list


def teacher_attendance_edit(request):
    context = get_error_context(request)
    if request.method == 'POST':
        date = parse_date(request.POST['date'])
        attendance_list = Attendance.objects.filter(date=date,
                                                    student__which_class__teacher__user=request.user).order_by(
            'student__roll_no')
        if 'edit' in request.POST:
            context['attendance_list'] = attendance_list
            # TODO request render(request, <template>, context)
        elif 'delete' in request.POST:
            attendance_list.delete()
        else:
            pass
    else:
        '''
        Form
        * Date -> name : date
        * 2 checkbox : edit, delete
        '''
        context = get_error_context(request)
        # TODO return render(request, <template>, context)

    return None


########################################################################################################################
#                                               Student Controller                                                     #
########################################################################################################################

'''
Views :
* Index - > show average attendance , average marks per subject, over all average marks, link to other views
* Check attendance at date -> form
* Check Test result
* Check Subject Tests
'''
