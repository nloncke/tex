from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.template import RequestContext, loader
from django_cas.decorators import login_required
from django_cas.views import login
from utils import *
from models import *
import re

@login_required
def account_index(request):
    from account.models import get_seller_offers
    from sell.utils import get_book_info
    result = []
    seller_id = 10
    seller_offers = get_seller_offers(seller_id)
    offers = {}
    for seller_offer in seller_offers:
        book_info = get_book_info(seller_offer.isbn)["book"]
        #offers["offer"] = {"title":book_info["title"], "price":seller_offer.price, "offer_id":seller_offer.offer_id}
        result.append({"title":book_info["title"], "price":seller_offer.price})
    return render(request,'account_index.html', {"offers":result})

def login(request):
    if request.user.is_authenticated():
        return render(request,'index.html')
    else:
        httpresp, user = login(request)        
        if is_registered(user):
            return httpresp

#         # Dummy for testing
#         from django.contrib import auth
#         user = auth.authenticate(username="tex", password="axal@tex")
#         auth.login(request, user)
        
        return register(request)

@login_required
def register(request):
    if request.method == 'POST':
        info["username"] = request.POST.get("username")
        info["password"] = request.POST.get("password")
        
        save_user(request.user, **info)
    return render(request,'account_register.html', {"registered": is_registered(request.user)})


def forbidden(request, template_name='403.html'):
    """Default 403 handler"""

    t = loader.get_template(template_name)
    return HttpResponseForbidden(t.render(RequestContext(request)))
