#for basic rendering of html pages
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

#for authentication login and logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from .models import *
from company.models import JAF, Category




def auth(user):
    return Student.objects.filter(user=user).exists()

# Create your views here.
def login(request):
    if request.POST :
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None and auth(user):  # A backend authenticated the credentials
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect('/student/home/')
        return render(request, "student/login.html",context={'error':'invalid credentials'})
    else:
        print(request.user.is_authenticated() and auth(request.user))
        if(request.user.is_authenticated() and auth(request.user)):
            return HttpResponseRedirect('/student/home/')
        else:
            return render(request, "student/login.html",context={'error':''})

@login_required()
def logout(request):
    if (not auth(request.user)):
        return redirect('/replace')
    auth_logout(request)
    return redirect('/replace')

@login_required(login_url='/student/login/')
def home(request):
    if (not auth(request.user)):
        return redirect('/replace')
    if request.method=="POST":
        print(request.POST)
        all_categorys = [category.type for category in Category.objects.all()]
        categorys = [key for key in request.POST.keys() if key in all_categorys]
        jaf_list = JAF.objects.all()
        jaf_list = jaf_list.filter(company__category__type__in=categorys)
    else:
        jaf_list = JAF.objects.all()
    data = {'jaf_list': jaf_list}
    return render(request, "student/home.html",  context=data)
