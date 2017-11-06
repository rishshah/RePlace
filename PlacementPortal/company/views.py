#for basic rendering of html pages
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

#for authentication login and logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from .models import *

# Create your views here.
def login(request):
	if request.POST :
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None and Company.objects.filter(user=user).count() == 1:  # A backend authenticated the credentials
			if user.is_active:
				auth_login(request, user)
				return HttpResponseRedirect('/company/home/')
		return render(request, "company/login.html",context={'error':'invalid credentials'})
	else:
		if(request.user.is_authenticated()):
			return HttpResponseRedirect('/company/home/')
		else:
			return render(request, "company/login.html",context={'error':''})

def register(request):
	if (request.method == "GET"):
		category_list = Category.objects.all()
		data = {'category_list':category_list}
		return render(request, "company/register.html", context = data)
	else:
		company_name = request.POST['company-name']
		password = request.POST['password']
		phone_number = request.POST['phone-number']
		category = request.POST['company-category']
		print(company_name, password, phone_number, category)
		return HttpResponse("Company Registered!")

@login_required()
def logout(request):
	data={'name':request.user.username}
	auth_logout(request)
	return render(request, "company/logout.html",context=data)

@login_required(login_url='/company/login/')
def home(request):
	return render(request, "company/home.html")