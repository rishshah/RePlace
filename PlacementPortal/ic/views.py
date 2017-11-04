from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("This is login IC.")

def login(request):
    return render(request,'ic/login.html')

def logout(request):
    return HttpResponse("This is logout IC")