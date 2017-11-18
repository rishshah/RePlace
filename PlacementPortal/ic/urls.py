from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'logout/$', views.logout, name='logout'),
    url(r'jaf/(?P<pk>[0-9]+)$', views.view_jaf, name='view_jaf'),
    url(r'resume/$', views.resume, name='resume'),
    url(r'$', views.home, name='home'),


]
