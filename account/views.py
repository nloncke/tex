from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.template import RequestContext, loader
from django_cas.decorators import login_required
from django_cas.views import login
from utils import *
import re

@login_required
def account_index(request):
    from account.models import get_seller_offers
    result = {}
    seller_id = 10
    result["Offers"] = get_seller_offers(seller_id)
    return render(request,'account_index.html', result)

def login(request):
    if request.user.is_authenticated():
        return render(request,'index.html', {"user":request.user.username})
    else:
#         return login(request)
        return register(request)


def register(request):
    registered = False
    
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Dummy for testing
        from django.contrib import auth
        user = auth.authenticate(username="tex", password="axal@tex")
        auth.login(request, user)
        
        registered = True
    return render(request,'account_register.html', {"registered": registered})


def forbidden(request, template_name='403.html'):
    """Default 403 handler"""

    t = loader.get_template(template_name)
    return HttpResponseForbidden(t.render(RequestContext(request)))
