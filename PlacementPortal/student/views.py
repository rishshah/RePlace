#for basic rendering of html pages
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

#for authentication login and logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.
def login(request):
	if request.POST :
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:  # A backend authenticated the credentials
			if user.is_active:
				auth_login(request, user)
				return HttpResponseRedirect('/student/home/')
		return render(request, "student/login.html",context={'error':'invalid credentials'})
	else:
		print(request.user.is_authenticated())
		if(request.user.is_authenticated()):
			return HttpResponseRedirect('/student/home/')
		else:
			return render(request, "student/login.html",context={'error':''})

@login_required()
def logout(request):
	data={'name':request.user.username}
	auth_logout(request)
	return render(request, "student/logout.html",context=data)

@login_required(login_url='/student/login/')
def home(request):
	return render(request, "student/home.html")