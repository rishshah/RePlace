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
from replace.models import *

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
		company = get_company(request.user)
		profile_name = request.POST.get("profile")
		description = request.POST.get("description")
		posting = request.POST.get("posting")
		resume_type = request.POST.get("resume_type")
		year = request.POST.get("year")
		duration = request.POST.get("duration")
		accomodation = request.POST.get("accomodation")
		other_details = request.POST.get("other_details")
		cpi_cutoff = request.POST.get("cpi_cutoff")
		stipend = request.POST.get("stipend")
		currency = request.POST.get("currency")
		department_list = request.POST.getlist("department")
		program_list = request.POST.getlist("program")

		
		return redirect("/company/")
	else :
		resume_type_list = Resume._meta.get_field("resume_number").choices
		job_profile_list = JobProfile.objects.all()
		program_list = Program.objects.all()
		department_list = Department.objects.all()
		test_type_list = TestType.objects.all()
		data = {'job_profile_list':job_profile_list,
		'resume_type_list':resume_type_list,
		'program_list':program_list,
		'department_list':department_list,
		'test_type_list':test_type_list}
		return render(request, "company/jaf_form.html", context=data )