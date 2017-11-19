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
from replace.models import Application

from django.utils.dateparse import parse_datetime

from .models import *
from company.models import *
from replace.models import *
from student.models import *


HOME_URL = '/'

def auth(user):
	return IC.objects.filter(user=user).exists()

# Create your views here.
@login_required()
def logout(request):
	if auth(request.user):
		auth_logout(request)
	return redirect(HOME_URL)
	
@login_required()
def home(request):
	if (not auth(request.user)):
		return redirect(HOME_URL)
	jaf_list = list(JAF.objects.all())
	for jaf in jaf_list:
		jaf.student_count  = Application.objects.filter(jaf = jaf).count()
	verified_students = Student.objects.filter(resume_verified = True)
	unverified_students = Student.objects.filter(resume_verified = False)
	data = {'jaf_list':jaf_list, 'verified_students':verified_students, 'unverified_students':unverified_students}
	return render(request, "ic/home.html", context = data)

@login_required()
def view_jaf(request,pk):
	if (not auth(request.user)):
		return redirect(HOME_URL)
	jaf = JAF.objects.get(pk = pk)
	if (jaf is None):
		return redirect(HOME_URL)
	application_list = Application.objects.filter(jaf = jaf)
	eligibility_list = Eligibility.objects.filter(jaf = jaf)

	program_list = set()
	department_list = set()
		
	for e in eligibility_list:	
		 program_list.add(e.program)
		 department_list.add(e.department)
	
	test_list = JAFTest.objects.filter(jaf = jaf)
	jaf.student_count = application_list.count()
	if (request.method == "POST"):
		test_fields = ["start_time","location","duration","description"]
		for test in test_list:
			for field in test_fields:
				field_name = str(test.test_number) + "-" + field
				field_value = request.POST.get(field_name)
				if (field == "start_time"):
					field_value = parse_datetime(field_value)
				setattr(test, field, field_value)
			test.save()

	data = {'jaf':jaf, 
			'application_list':application_list, 
			'eligibility_list':eligibility_list, 
			'program_list': program_list,
			'department_list': department_list,
			'test_list': test_list
			}
	print(eligibility_list)
	return render(request, "ic/jaf.html", context = data)


@login_required()
def resume(request):
	if (not auth(request.user)):
		return redirect(HOME_URL)
	verified_students = Student.objects.filter(resume_verified = True)
	unverified_students = Student.objects.filter(resume_verified = False)
	data = {'verified_students':verified_students, 'unverified_students':unverified_students}
	return render(request, "ic/resume.html", context = data)
