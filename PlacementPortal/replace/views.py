#for basic rendering of html pages
from django.http import HttpResponse

# Create your views here.
def index(request):
	return HttpResponse("My Home Page")