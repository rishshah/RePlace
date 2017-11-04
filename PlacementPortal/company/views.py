from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
def login(request):
	if (request.method == 'GET'):
		return render(request, "company/login.html")
	elif (request.method == 'POST'):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password = password)
		if (user is not None):
			login(request, user)
			return HttpResponse("Login Success")
		else:
			return HttpResponse("Invalid Credentials")

@login_required(login_url = '/company/login')
def logout(request):
	logout(request)
	return HttpResponse("Logout Success")
	#return render(request, "company/login.html")


def register(request):
	return render(request, "company/register.html")