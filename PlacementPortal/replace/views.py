#for basic rendering of html pages
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

#for authentication login and logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from student.models import *;
from ic.models import *;
from company.models import *;

def auth_student(user):
    return Student.objects.filter(user=user).exists()
def auth_ic(user):
    return IC.objects.filter(user=user).exists()
def auth_company(user):
    return Company.objects.filter(user=user).exists()

# Create your views here.
def index(request):
	return render(request, "replace/index.html")

def login(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:  # A backend authenticated the credentials
            if user.is_active:
                auth_login(request, user)

                if auth_student(user):
                	return HttpResponseRedirect('/student/')
                elif auth_ic(user):
                	return HttpResponseRedirect('/ic/')
                elif auth_company(user):
                	return HttpResponseRedirect('/company/')
            
       	return render(request, "replace/login.html",context={'error':'invalid credentials'})
    else:
        if request.user.is_authenticated():
            if auth_student(request.user):
            	return HttpResponseRedirect('/student/')
            elif auth_ic(request.user):
            	return HttpResponseRedirect('/ic/')
            elif auth_company(request.user):
            	return HttpResponseRedirect('/company/')
            else:
            	return render(request, "replace/login.html",context={'error':'forbidden'})
        else:
        	return render(request, "replace/login.html",context={'error':''})

def register(request):
	category_list = Category.objects.all()
	if (request.method == "GET"):
		data = {'tab':'register','category_list':category_list,'error':''}
		return render(request, "replace/register.html", context = data)
	else:
		company_name = request.POST['company-name']
		company_username = request.POST['company-username']
		password = request.POST['password']
		phone_number = request.POST['phone-number']
		category_name = request.POST['company-category']
		category = Category.objects.get(type = category_name)
		if (Company.objects.filter(name = company_name).exists()):
			print ("duplicate company name")
			data = {'tab':'register','category_list':category_list,'error':'company name already exists'}
			return render(request, "replace/register.html", context = data)
		if (User.objects.filter(username = company_username).exists()):
			print ("duplicate username")
			data = {'tab':'register','category_list':category_list,'error':'username already exists'}
			return render(request, "replace/register.html", context = data)
		if (category is None):
			print ("invalid category")
			data = {'tab':'register','category_list':category_list,'error':'invalid category'}
			return render(request, "replace/register.html", context = data)
		user = User.objects.create_user(username = company_username, password = password)
		user.save()
		company = Company(name = company_name, user = user, phone_number = phone_number, category = category)
		company.save()
		print(company_name, company_username, password, phone_number, category)
		data = {'tab':'login','category_list':category_list,'error':''}
		return render(request, "replace/login.html", context = data)