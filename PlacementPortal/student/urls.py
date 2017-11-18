from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'jafs/$', views.see_jafs, name='see_jafs'),
    url(r'upload_resume/$', views.upload_resume, name='upload_resume'),
    url(r'logout/$', views.logout, name='logout'),
    url(r'$', views.home, name='home'),
]