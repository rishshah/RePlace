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

def auth(user):
	return Company.objects.filter(user=user).exists()

# Create your views here.
def login(request):
	category_list = Category.objects.all()
	if request.POST :
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None and auth(user):  # A backend authenticated the credentials
			if user.is_active:
				auth_login(request, user)
				return HttpResponseRedirect('/company/home/')
		data = {'tab':'login','category_list':category_list,'error':'invalid credentials'}
		return render(request, "company/login.html",context=data)
	else:
		if(request.user.is_authenticated()):
			return HttpResponseRedirect('/company/home/')
		else:
			data = {'tab':'login','category_list':category_list,'error':''}
			return render(request, "company/login.html",context=data)

def register(request):
	category_list = Category.objects.all()
	if (request.method == "GET"):
		data = {'tab':'register','category_list':category_list,'error':''}
		return render(request, "company/login.html", context = data)
	else:
		company_name = request.POST['company-name']
		company_username = request.POST['company-username']
		password = request.POST['password']
		phone_number = request.POST['phone-number']
		category = request.POST['company-category']
		if (Company.object.filter(name = company_name).exists()):
			print ("duplicate company name")
			data = {'tab':'register','category_list':category_list,'error':'company name already exists'}
			return render(request, "company/login.html", context = data)
		if (User.objects.filter(username = company_username).exists()):
			print ("duplicate username")
			data = {'tab':'register','category_list':category_list,'error':'username already exists'}
			return render(request, "company/login.html", context = data)
		user = User.objects.create(username = company_username, password = password)
		user.save()
		company = Company(name = company_name, user = user, phone_number = phone_number, category = category)
		company.save()
		print(company_name, company_username, password, phone_number, category)
		data = {'tab':'login','category_list':category_list,'error':''}
		return render(request, "company/login.html", context = data)

@login_required()
def logout(request):
	if (not auth(request.user)):
		return redirect('/replace')
	auth_logout(request)
	return redirect('/replace')

@login_required(login_url='/company/login/')
def home(request):
	if (not auth(request.user)):
		return redirect('/replace')
	return render(request, "company/home.html")