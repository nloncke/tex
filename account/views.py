from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.template import RequestContext, loader
from utils import *
import re

# render(request, html template, function that returns dictionary)
# render(-, nicole, jeffrey)
def account_index(request):
    return render(request,'account_index.html')


def forbidden(request, template_name='403.html'):
    """Default 403 handler"""

    t = loader.get_template(template_name)
    return HttpResponseForbidden(t.render(RequestContext(request)))
