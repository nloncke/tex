from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.template import RequestContext, loader
from utils import *
from models import *
import re

alpha = ["jasala","lauraxu"]

def account_index(request):
    from account.models import get_seller_offers, get_seller_auctions, get_follow_list, unfollow
    from buy.models import remove_offer, remove_auction
    from sell.utils import get_book_info
    from book.utils import get_book
    # only post if removing offer
    if request.method == "POST": 
        action = request.POST.get("action", "")
        if action == "remove_auction":
            auction_id = request.POST.get("auction_id", "0")
            removed_auction = remove_auction(auction_id, False)
        elif action == "remove_offer":
            offer_id = request.POST.get("offer_id", "0")
            sold_offer = remove_offer(offer_id) 
        elif action == "unfollow":     
            isbn = request.POST.get("target_isbn", "0")
            user = request.user
            if validate_isbn(isbn):
                unfollow(user=user, isbn=isbn)  
        else:
            pass # or throw error because shouldn't get here?
   
    result_offers = []
    result_auctions = []
    result_follow = []
    seller_id = request.user.username
    user = request.user
    seller_offers = get_seller_offers(seller_id)
    seller_auctions = get_seller_auctions(seller_id)
    offers = {}
    for seller_offer in seller_offers:
        book_info = get_book_info(seller_offer.isbn)["book"]
        result_offers.append({"title":book_info["title"], "price":seller_offer.price, "offer_id":seller_offer.id,
                       "isbn":seller_offer.isbn})
    auctions = {}
    for seller_auction in seller_auctions:
        book_info = get_book_info(seller_auction.isbn)["book"]
        result_auctions.append({"title":book_info["title"], "current_price":seller_auction.current_price, "auction_id":seller_auction.id,
                       "isbn":seller_auction.isbn, "end_time":seller_auction.end_time})
    
    follow_isbns = get_follow_list(user=user)   

    min_offer = {}
    min_auction = {}
    for isbn in follow_isbns:
        if isbn:
            book_info = get_book(isbn)
            offers = book_info["offers"]
            auctions = book_info["auctions"]
            if offers:
                min_offer = offers[0]
            if auctions:
                min_auction = auctions[0]
            result_follow.append({"isbn":isbn, "book":book_info["book"], "min_offer":min_offer, "min_auction":min_auction})
          
    
    return render(request,'account_index.html', {"offers":result_offers, "auctions":result_auctions, "follows":result_follow})

def login(request):
    from django_cas.views import login, logout
    
#   For local dev  
    from django.contrib import auth
    from account.models import BookUser, is_registered
    user = auth.authenticate(username="tex", password="axal@tex")
    if not is_registered(user):
        bu = BookUser(user=user, watch_list='', default_search='author', class_year='')
        bu.save()  
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
        info["class_year"] = request.POST.get("class_year")
        info["default_search"] = request.POST.get("default_search")
        
        save_user(request.user, **info)
    return render(request,'account_profile.html')

def forbidden(request, template_name='403.html'):
    """Default 403 handler"""

    t = loader.get_template(template_name)
    return HttpResponseForbidden(t.render(RequestContext(request)))


