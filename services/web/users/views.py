from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
#default view if user views the /users page
def index(request):
    return HttpResponse("If you stumbled on this page, please use api to access this feature.")
