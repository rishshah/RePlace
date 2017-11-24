from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from .models import *
from company.models import *
from replace.models import *
from student.models import *


import os,datetime
from django.utils import timezone
import datetime
now = datetime.datetime.now()

HOME_URL = '/login/'

def auth(user):
    return Student.objects.filter(user=user).exists()

def get_student(user):
    return Student.objects.get(user = user)

def is_eligible(student, jaf):
    cansign_eligibility = Eligibility.objects.filter(jaf=jaf, department=student.department, program=student.program)
    if len(cansign_eligibility) == 1 and cansign_eligibility[0].jaf.cpi_cutoff <= student.cpi:
        application = Application.objects.filter(jaf=jaf,student=student)
        if len(application) == 1:
            if application[0].is_selected:
                return 'Already selected', 'green'
            else:
                for app in  Application.objects.filter(student=student):
                    if app.is_selected and app.jaf.job_year == datetime.datetime.now().year:
                        return 'Already Employed','orange'
                return 'Signed','green'

        elif cansign_eligibility[0].jaf.deadline >= timezone.now():
            for app in  Application.objects.filter(student=student):
                if app.is_selected and app.jaf.job_year == datetime.datetime.now().year:
                    return 'Already Employed','orange'
            return 'Can Sign','blue'
        else:
            return 'Past Deadline','grey'
    else:
        return 'Not Eligible','red' 

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
def selections(request):
    if (not auth(request.user)):
        return redirect(HOME_URL)
    
    final_selection_jaf_list = []
    for jaf in JAF.objects.all().order_by('deadline'):
        selected_applications = Application.objects.filter(jaf = jaf, is_selected = True)
        selected_students = []
        for application in selected_applications:
            selected_students.append(application.student.name)
        jaf.selected_student_list = selected_students;
        if len(selected_students) > 0 :
            final_selection_jaf_list.append(jaf)  

    data = {'final_selection_jaf_list': final_selection_jaf_list}        
    return render(request, "student/selections.html", context=data)

    
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

    if request.method=="POST":

        if 'cansign' in request.POST.keys():
            print(1)
            jaf_list = jaf_list.filter(eligibility__department=student.department, eligibility__program=student.program, cpi_cutoff__lt=student.cpi, deadline__lt=datetime.date.today())

        if 'signed' in request.POST.keys():
            print(2)
            jaf_list = jaf_list.filter(application__student=student)

        if 'pre_deadline' in request.POST.keys():
            print(3)
            jaf_list = jaf_list.filter(deadline__gt=datetime.date.today())

        try:
            min_stipend = float(request.POST['minstipend'])
            max_stipend = float(request.POST['maxstipend'])
            print(4)
            jaf_list = jaf_list.filter(stipend__gt=min_stipend, stipend__lt=max_stipend)
        except:
            pass

        try:
            min_cpi = float(request.POST['mincpi'])
            max_cpi = float(request.POST['maxcpi'])
            print(5)
            jaf_list = jaf_list.filter(cpi_cutoff__gt=min_cpi, cpi_cutoff__lt=max_cpi)
        except:
            pass

        if 'job_profile' in request.POST:
            jaf_list = jaf_list.filter(profile__name__in=request.POST.getlist('job_profile'))
        if 'company_category' in request.POST:
            jaf_list = jaf_list.filter(company__category__type__in=request.POST.getlist('company_category'))

        print(request.POST)


    for jaf in jaf_list:
        jaf.student_count  = Application.objects.filter(jaf = jaf).count()
        jaf.eligibility,jaf.eligibility_color = is_eligible(student,jaf)

    data = {'jaf_list': jaf_list,
            'job_profile_list': JobProfile.objects.all(),
            'company_category_list':Category.objects.all()
            }
    return render(request, "student/jaf_list.html", context=data)

@login_required()
def sign_jaf(request):
    if not auth(request.user):
        return redirect(HOME_URL)

    student = get_student(request.user);
    if (request.method == "POST"):
        jaf = JAF.objects.get(id = request.POST.get("jaf_id"))
        if is_eligible(student, jaf)[0] == 'Can Sign':
            application = Application(student = student, jaf = jaf)
            application.save()
        return redirect('/student/see_jafs/')

@login_required()
def unsign_jaf(request):
    if not auth(request.user):
        return redirect(HOME_URL)

    student = get_student(request.user)
    if (request.method == "POST"):
        jaf = JAF.objects.get(id = request.POST.get("jaf_id"))
        if is_eligible(student, jaf)[0] == 'Signed':
            application = Application.objects.get(student = student, jaf = jaf)
            application.delete()
        return redirect('/student/see_jafs/')

@login_required()
def view_jaf(request,pk):
    if (not auth(request.user)):
        return redirect(HOME_URL)
    jaf = JAF.objects.get(pk = pk)
    if (jaf is None):
        return redirect(HOME_URL)
    eligibility_list = Eligibility.objects.filter(jaf = jaf)

    program_list = set()
    department_list = set()
        
    for e in eligibility_list:  
         program_list.add(e.program)
         department_list.add(e.department)
    
    test_list = JAFTest.objects.filter(jaf = jaf)
    jaf.student_count = Application.objects.filter(jaf = jaf).count()
    signing_status = is_eligible(get_student(request.user),jaf)[0]
    related_jaf_list = JAF.objects.filter(company=jaf.company, job_year__lt=jaf.job_year)
    # related_jaf_list = JAF.objects.all()#(company=jaf.company, profile=jaf.profile)
    data = {'jaf':jaf, 
            'eligibility_list':eligibility_list, 
            'program_list': program_list,
            'department_list': department_list,
            'test_list': test_list,
            'status': signing_status,
            'related_jaf_list':related_jaf_list
            }

    return render(request, "student/student_view_jaf.html", context = data)

def related_jaf_view(request, jaf_id):
    jaf = JAF.objects.filter(id= jaf_id)[0]
    test_list = JAFTest.objects.filter(jaf = jaf)
    selection_list = Application.objects.filter(jaf = jaf, is_selected=True)
    count_selected = len(selection_list)
    count_applied = Application.objects.filter(jaf = jaf).count()
    data = {'jaf':jaf,
            'selection_list': selection_list,
            'count_applied': count_applied,
            'count_selected': count_selected,
            'test_list': test_list
        }
    return render(request, "student/related_view_jaf.html", context = data)