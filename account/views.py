from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.template import RequestContext, loader
from django_cas.decorators import login_required
from utils import *
from models import *
import re

@login_required
def account_index(request):
    from account.models import get_seller_offers#, get_follow_list
    from buy.models import remove_offer
    from sell.utils import get_book_info
    # only post if removing offer
    if request.method == "POST": 
        offer_id = request.POST.get("offer_id", "0")
        sold_offer = remove_offer(offer_id)        
    result = []
    seller_id = request.user.username
    user = request.user
    seller_offers = get_seller_offers(seller_id)
    offers = {}
    #follow_list = get_follow_list(user=user)
    for seller_offer in seller_offers:
        book_info = get_book_info(seller_offer.isbn)["book"]
        result.append({"title":book_info["title"], "price":seller_offer.price, "offer_id":seller_offer.id})
    return render(request,'account_index.html', {"offers":result, "follow_list":"test"})

def login(request):
    from django_cas.views import login
    if request.user.is_authenticated():
        return render(request,'index.html')
    else:
        # Dummy for testing
        from django.contrib import auth
        user = auth.authenticate(username="tex", password="axal@tex")
        auth.login(request, user)      
        
        return login(request)        



@login_required
def profile(request):
    if request.method == 'POST':
        info["username"] = request.POST.get("username")
        info["password"] = request.POST.get("password")
        
        save_user(request.user, **info)
    return render(request,'account_profile.html')

def forbidden(request, template_name='403.html'):
    """Default 403 handler"""

    t = loader.get_template(template_name)
    return HttpResponseForbidden(t.render(RequestContext(request)))


