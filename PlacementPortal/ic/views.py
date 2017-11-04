from django.shortcuts import render

# Create your views here.
def login(request, question_id):
    return HttpResponse("This is login IC.")

def logout(request, question_id):
    return HttpResponse("This is logout IC")