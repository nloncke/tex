from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.template import RequestContext, loader
from utils import *
from models import *
import re

alpha = ["jasala","lauraxu"]

def account_index(request):
    from account.models import get_seller_offers, get_seller_auctions#, get_follow_list
    from buy.models import remove_offer
    from sell.utils import get_book_info
    # only post if removing offer
    if request.method == "POST": 
        offer_id = request.POST.get("offer_id", "0")
        sold_offer = remove_offer(offer_id)        
    result_offers = []
    result_auctions = []
    seller_id = request.user.username
    user = request.user
    seller_offers = get_seller_offers(seller_id)
    seller_auctions = get_seller_auctions(seller_id)
    offers = {}
    #follow_list = get_follow_list(user=user)
    for seller_offer in seller_offers:
        book_info = get_book_info(seller_offer.isbn)["book"]
        result_offers.append({"title":book_info["title"], "price":seller_offer.price, "offer_id":seller_offer.id,
                       "isbn":seller_offer.isbn})
    auctions = {}
    for seller_auction in seller_auctions:
        book_info = get_book_info(seller_auction.isbn)["book"]
        result_auctions.append({"title":book_info["title"], "current_price":seller_auction.current_price, "auction_id":seller_auction.id,
                       "isbn":seller_auction.isbn, "end_time":seller_auction.end_time})
        
    return render(request,'account_index.html', {"offers":result_offers, "auctions":result_auctions, "follow_list":"test"})

def login(request):
    from django_cas.views import login, logout
    
#   For local dev  
    from django.contrib import auth
    user = auth.authenticate(username="tex", password="axal@tex")
    auth.login(request, user) 
    return login(request)
    
# for Alpha testers    
    httpresp = login(request)
    if request.user.is_authenticated():
        if request.user.username not in alpha:
            httperror = render(request,'alpha_test.html')
            logout(request)
            return httperror
    return httpresp
    

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


