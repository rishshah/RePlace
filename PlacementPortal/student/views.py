from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from .models import *
from company.models import JAF, Category

HOME_URL = '/'

def auth(user):
    return Student.objects.filter(user=user).exists()

def get_student(user):
    return Student.objects.get(user = user)

@login_required()
def logout(request):
    if auth(request.user):
        auth_logout(request)
    return redirect(HOME_URL)

@login_required()
def home(request):
    if (not auth(request.user)):
        return redirect(HOME_URL)
    student = get_student(request.user)
    data = {'student': student}    
    return render(request, "student/home.html", context=data)

@login_required()
def upload_resume(request):
    if (not auth(request.user)):
        return redirect(HOME_URL)
    if (request.method=="POST"):
        student = get_student(request.user)
        resume_number = {"one-page":0, "two-page-tech":1, "two-page-non-tech":2, "cv":3}
        print (student.name, request.FILES)
        for resume_type in resume_number:
            print (resume_type, resume_number[resume_type])
            resume_file = request.FILES.get(resume_type)
            print (resume_file)
            if (resume_file is not None):
                resume = Resume.objects.get(student = student, resume_number = resume_number[resume_type])
                if (resume is None):
                    resume = Resume(student = student, resume_number = resume_number[resume_type]) 
                resume.file = resume_file
                resume.save()
                print ("resume saved")
        return redirect('/student/')
    else:
        pass

@login_required()
def my_jobs(request):
    if (not auth(request.user)):
        return redirect(HOME_URL)
    if request.method=="GET":
        jaf_list = JAF.objects.all()
        data = {'jaf_list': jaf_list}
        return render(request, "student/my_jobs.html", context=data)
    else:
        pass

@login_required()
def see_jafs(request):
    if not auth(request.user):
        return redirect(HOME_URL)

    student = get_student(request.user)
    jaf_list = JAF.objects.all()

    if request.method=="POST":
        print(request.POST)
        all_categorys = [category.type for category in Category.objects.all()]
        categorys = [key for key in request.POST.keys() if key in all_categorys]
        jaf_list = jaf_list.filter(company__category__type__in=categorys)

        if 'cansign' in request.POST.keys():
            jaf_list = jaf_list.filter(eligibility__department=student.department, eligibility__program=student.program, eligibility__cpi_cutoff__lt=student.cpi)

        if 'signed' in request.POST.keys():
            jaf_list = jaf_list.filter(application__student=student)

    data = {'jaf_list': jaf_list}
    return render(request, "student/jaf_list.html", context=data)
