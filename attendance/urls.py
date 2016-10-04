import django.contrib.auth.views
from django.conf.urls import url

from attendance import views
from attendance.views import validate_login, common_login, admin_teacher_add, admin_index

urlpatterns = [
    url(r'^$', common_login, name='login'),
    url(r'^login/validate/$', validate_login, name='login_validate'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^change/password/$', views.change_password, name='change_password'),
    # ------------------ Admin ---------------------------------------

    url(r'^admin/$', admin_index, name="admin_index"),
    url(r'^admin/teacher/add/$', admin_teacher_add, name='admin_teacher_add'),
    url(r'^admin/teacher/remove/$', views.admin_teacher_remove, name='admin_teacher_delete'),
    url(r'admin/teacher/edit/$', views.admin_teacher_edit, name='admin_teacher_edit'),
    url(r'^admin/class/add/$', views.admin_class_add, name='admin_class_add'),
    url(r'admin/class/remove/$', views.admin_class_remove, name='admin_class_remove'),

    # ------------------ Teacher --------------------------------------

    url(r'^teacher/$', views.teacher_index, name="teacher_index"),
    url(r'^teacher/student/add/$', views.teacher_add_student, name="teacher_student_add"),
    url(r'^teacher/student/remove/$', views.teacher_remove_student, name="teacher_student_remove"),
    url(r'^teacher/student/edit/$', views.teacher_student_edit, name="teacher_student_edit"),
    url(r'teacher/subject/add/$', views.teacher_subject_add, name="teacher_subject_add"),
    url(r'^teacher/subject/edit/$', views.teacher_subject_edit, name="teacher_subject_edit"),

    url(r'^teacher/test/add/$', views.teacher_test_add, name="teacher_test_add"),
    url(r'^teacher/test/edit/$', views.teacher_test_edit, name="teacher_test_select"),
    # test remove merged with edit
    url(r'^teacher/attendance/$', views.teacher_attendance_today, name="teacher_attendance_today"),
    url(r'^teacher/attendance/edit/$', views.teacher_attendance_edit, name="teacher_attendance_edit"),
    # remove attendance merged with edit

    url(r'teacher/report/student/$', views.teacher_report_view_single, name="teacher_report_single"),
    url(r'teacher/report/class/$', views.teacher_report_class, name="teacher_report_class"),

    # -------------------- Student --------------------------------------
    url(r'student/$',views.student_index,name="student_index"),

    # ---------------------Principal---------------------------------------
    url(r'principal/$', views.principal_index, name="principal_index")
]
