import django.contrib.auth.views
from django.conf.urls import url

from attendance import views
from attendance.views import validate_login, common_login, admin_teacher_add, admin_index

urlpatterns = [
    url(r'^$', common_login, name='login'),
    url(r'^login/validate/$', validate_login, name='login_validate'),
    url(r'^admin/$', admin_index, name="admin_index"),
    url(r'^admin/teacher/add/$', admin_teacher_add, name='admin_teacher_add'),
    url(r'admin/class/add', views.admin_class_add, name='admin_class_add'),
    url(r'^logout/$', django.contrib.auth.views.logout, name='logout'),
]