from django.shortcuts import render
from django.http import HttpResponse
from utils import *
from django.shortcuts import render_to_response

# render(request, html template, function that returns dictionary)
# render(-, nicole, jeffrey)
def index(request):
    return render_to_response('index.html')

def results(request):
    pass
    #return render(request, 'search_results.html', hello())
    