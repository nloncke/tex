from django.shortcuts import render
from django.http import HttpResponse
from utils import *
import re

# render(request, html template, function that returns dictionary)
# render(-, nicole, jeffrey)
def account_index(request):
    return render(request,'account_index.html')