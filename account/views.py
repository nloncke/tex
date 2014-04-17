from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.template import RequestContext, loader
from django.contrib.auth import login
from utils import *
import re

# render(request, html template, function that returns dictionary)
# render(-, nicole, jeffrey)
def account_index(request):
    from account.models import get_seller_offers
    result = {}
    seller_id = 10
    result["Offers"] = get_seller_offers(seller_id)
    return render(request,'account_index.html', result)

def validate(request):
    return render(request,'index.html')


def register(request):
    registered = False
    
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        registered = True
    return render(request,'account_register.html', {"registered": registered})


def forbidden(request, template_name='403.html'):
    """Default 403 handler"""

    t = loader.get_template(template_name)
    return HttpResponseForbidden(t.render(RequestContext(request)))
