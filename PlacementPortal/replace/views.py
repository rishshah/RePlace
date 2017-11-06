#for basic rendering of html pages
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def index(request):
	return render(request, "replace/index.html")