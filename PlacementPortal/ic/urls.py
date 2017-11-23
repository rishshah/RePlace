from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'logout/$', views.logout, name='logout'),
    url(r'jaf/(?P<pk>[0-9]+)$', views.view_jaf, name='view_jaf'),
    url(r'verification/(?P<pk>[0-9]+)/(?P<status>[0-9]+)$', views.student_verification, name='student_verification'),
    url(r'resume/$', views.verify_resume, name='resume'),
    url(r'view_resume/(?P<id>[0-9]+)/(?P<resume_number>[0-9]+)$', views.view_resume, name='view_resume'),
    url(r'$', views.home, name='home'),


]
