from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from .models import *
from company.models import JAF, Category
import os

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
        resume_dict = {"one-page":0, "two-page-tech":1, "two-page-non-tech":2, "cv":3}
        print (student.name, request.FILES)
        for resume_type in resume_dict:
            print (resume_type, resume_dict[resume_type])
            resume_file = request.FILES.get(resume_type)
            print (resume_file)
            if (resume_file is not None):
                try:
                    resume = Resume.objects.get(student = student, resume_number = resume_dict[resume_type])
                except:
                    resume = None
                if (resume is None):
                    resume = Resume(student = student, resume_number = resume_dict[resume_type]) 
                else:
                    try:
                        os.remove(resume.file.path)
                    except:
                        pass
                resume.file = resume_file
                resume.file.name = student.roll_number+"-"+str(resume_dict[resume_type])+".pdf"
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
        selection_list = Application.objects.filter(is_selected=True, student=get_student(request.user))
        data = {'selection_list': selection_list}
        return render(request, "student/my_jobs.html", context=data)
    else:
        jaf = JAF.objects.get(id=request.POST["id"])
        application = Application.objects.get(jaf=jaf, is_selected=True, student=get_student(request.user))
        application.review = request.POST['review']
        application.save();
        return redirect("/student/my_jobs/")

@login_required()
def see_jafs(request):
    if not auth(request.user):
        return redirect(HOME_URL)

    student = get_student(request.user)
    jaf_list = JAF.objects.all()

    print("1")
    for jaf in jaf_list:
        print(jaf)

    if request.method=="POST":
        print(request.POST)
        all_categorys = [category.type for category in Category.objects.all()]
        categorys = [key for key in request.POST.keys() if key in all_categorys]
        jaf_list = jaf_list.filter(company__category__type__in=categorys)

        if 'cansign' in request.POST.keys():
            jaf_list = jaf_list.filter(eligibility__department=student.department, eligibility__program=student.program, cpi_cutoff__lt=student.cpi)

        if 'signed' in request.POST.keys():
            jaf_list = jaf_list.filter(application__student=student)

        try:
            min_stipend = float(request.POST['minstipend'])
            max_stipend = float(request.POST['maxstipend'])
            jaf_list = jaf_list.filter(stipend__gt=min_stipend, stipend__lt=max_stipend)
        except:
            pass

        try:
            min_cpi = float(request.POST['mincpi'])
            max_cpi = float(request.POST['maxcpi'])
            jaf_list = jaf_list.filter(cpi_cutoff__gt=min_cpi, cpi_cutoff__lt=max_cpi)
        except:
            pass

    data = {'jaf_list': jaf_list}
    return render(request, "student/jaf_list.html", context=data)

@login_required()
def sign_jafs(request):
    if not auth(request.user):
        return redirect(HOME_URL)

    if (request.method == "POST"):
        student = get_student(request.user)
        jaf_id = request.POST.get("jaf_id")
        jaf = JAF.objects.get(id = jaf_id)
        application = Application(student = student, jaf = jaf)
        application.save()
        return redirect('/student/')