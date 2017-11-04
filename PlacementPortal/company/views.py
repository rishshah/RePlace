from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def login(request):
	return HttpResponse("Login Page")

def logout(request):
	return HttpResponse("Logout Page")

def register(request):
	return HttpResponse("Registration Page")