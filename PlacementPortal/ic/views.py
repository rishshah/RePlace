#for basic rendering of html pages
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

#for authentication login and logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from company.models import JAF
from student.models import Student

from .models import *

def auth(user):
	return IC.objects.filter(user=user).exists()


# Create your views here.
def login(request):
	if request.POST :
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None and auth(user):  # A backend authenticated the credentials
			if user.is_active:
				auth_login(request, user)
				return HttpResponseRedirect('/ic/home/')
		return render(request, "ic/login.html",context={'error':'invalid credentials'})
	else:
		if(request.user.is_authenticated()):
			return HttpResponseRedirect('/ic/home/')
		else:
			return render(request, "ic/login.html",context={'error':''})

@login_required()
def logout(request):
	if (not auth(request.user)):
		return redirect('/replace')
	auth_logout(request)
	return redirect('/replace')

@login_required(login_url='/ic/login/')
def home(request):
	if (not auth(request.user)):
		return redirect('/replace')
	jaf_list = JAF.objects.all()
	verified_students = Student.objects.filter(resume_verified = True)
	unverified_students = Student.objects.filter(resume_verified = False)
	data = {'jaf_list':jaf_list, 'verified_students':verified_students, 'unverified_students':unverified_students}
	return render(request, "ic/home.html", context = data)