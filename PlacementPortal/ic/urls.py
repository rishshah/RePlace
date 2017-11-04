from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^Login/$', views.login, name='login'),
    url(r'^Logout/$', views.logout, name='logout'),

]