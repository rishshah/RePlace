from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'jafs/$', views.see_jafs, name='see_jafs'),
    url(r'jaf/(?P<pk>[0-9]+)$', views.view_jaf, name='view_jaf'),
    url(r'upload_resume/$', views.upload_resume, name='upload_resume'),
    url(r'unsign/$', views.unsign_jaf, name='unsign_jaf'),
    url(r'sign/$', views.sign_jaf, name='sign_jaf'),
    url(r'logout/$', views.logout, name='logout'),
    url(r'jobs/$', views.my_jobs, name='my_jobs'),
    url(r'$', views.home, name='home'),
]