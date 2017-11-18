#for basic rendering of html pages
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

#for authentication login and logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from student.models import *
from replace.models import Application

HOME_URL = '/'

def auth(user):
	return Company.objects.filter(user=user).exists()

def get_company(user):
	return Company.objects.get(user = user)

@login_required()
def logout(request):
	if (auth(request.user)):
		auth_logout(request)
	return redirect(HOME_URL)

@login_required()
def home(request):
	if (not auth(request.user)):
		return redirect(HOME_URL)
	company = get_company(request.user)	
	jaf_list = JAF.objects.filter(company = company)
	for jaf in jaf_list:
		jaf.student_count  = Application.objects.filter(jaf = jaf).count()
	data = {"jaf_list":jaf_list}
	return render(request, "company/home.html", context = data)

@login_required()
def new_jaf(request):
	if (not auth(request.user)):
		return redirect(HOME_URL)
	if request.method == "POST" :
		return render(request, "company/jaf_form.html")
	else :
		data = {'job_profile_list':JobProfile.objects.all()}
		return render(request, "company/jaf_form.html", context=data )