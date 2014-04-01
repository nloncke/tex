from django.shortcuts import render
from django.http import HttpResponse
from utils import *
from django.shortcuts import render_to_response

def index(request):
    return render_to_response('hello.html')

def result(request):
#     request.POST.get("read_in", "")
    return render(request, 'hellodisplay.html', {"output": request.POST.get("read_in", "NONE FOUND")}) 
    