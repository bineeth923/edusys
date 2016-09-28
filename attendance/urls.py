import django.contrib.auth.views
from django.conf.urls import url

from attendance import views
from attendance.views import validate_login, common_login, admin_teacher_add, admin_index

urlpatterns = [
    url(r'^$', common_login, name='login'),
    url(r'^login/validate/$', validate_login, name='login_validate'),
    url(r'^logout/$', views.logout_user, name='logout'),

    ################### Admin #########################################

    url(r'^admin/$', admin_index, name="admin_index"),
    url(r'^admin/teacher/add/$', admin_teacher_add, name='admin_teacher_add'),
    url(r'^admin/teacher/remove/$', views.admin_teacher_remove, name='admin_teacher_delete'),
    url(r'^admin/class/add', views.admin_class_add, name='admin_class_add'),
    url(r'admin/class/remove', views.admin_class_remove, name='admin_class_remove'),

    ################### Teacher ########################################

    url(r'^teacher/$', views.teacher_index, name="teacher_index"),
    url(r'^teacher/student/add', views.teacher_add_student, name="teacher_student_add"),
    url(r'^teacher/student/remove', views.teacher_remove_student, name="teacher_student_remove"),
    url(r'^teacher/student/edit',views.teacher_student_edit, name="teacher_student_edit"),
    # TODO test
    url(r'^teacher/test/add', views.teacher_test_add, name="teacher_test_add"),

        # TODO test edit
        # TODO test remove
    url(r'teacher/attendance', views.teacher_attendance_today, name="teacher_attendance")
    # TODO attendance
        # TODO edit attendace
        # TODO remove attendance
    # TODO report
        # TODO Individual
        # TODO Class
    ################### Student #########################################


]
