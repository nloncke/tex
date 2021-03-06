from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.template import RequestContext, loader
import re

testers = ["jasala","lauraxu", "nloncke", "yoyeh", "kohemeng",
    "hmccormi", "swatters", "salberti", "fpina", "yunzhil",
    "dkoltuny", "lslosar", "abuddhir", "afyabrou", "cgordon",
    "mmedward", "lberdick", "morgant", "echeruiy", "ethill",
    "rdaker", "mwirth", "gdsheppe", "jgsamuel", "pmoon", "aabdelaz"
    , "splichte", "sgichohi", "bwk", "cmoretti", "soumyade",
     "raghavs", "twoh", "xinjin", "rtilahun"]

def account_index(request):
    from account.models import get_seller_offers, get_seller_auctions, get_follow_list, unfollow, save_user
    from buy.models import remove_offer, remove_auction
    from sell.utils import get_book_info
    from book.utils import get_book
    from search.utils import validate_isbn
    
    # only post if removing offer
    if request.method == "POST": 
        action = request.POST.get("action", "")
        if action == "remove_offer":
            offer_id = request.POST.get("offer_id", "0")
            remove_offer(offer_id=offer_id) 
        elif action == "unfollow":     
            isbn = request.POST.get("target_isbn", "0")
            user = request.user
            if validate_isbn(isbn=isbn):
                unfollow(user=user, isbn=isbn) 
        elif action == "update":
            info = {"class_year": request.POST.get("class_year")}
            info["default_search"] = request.POST.get("default_search")
            save_user(request.user, **info)
        else:
            return render(request, 'error_page.html')
   
    result_offers = []
    result_auctions = []
    result_follow = []
    seller_id = request.user.username
    user = request.user
 
    seller_offers = get_seller_offers(seller_id=seller_id)
    offers = {}
    for seller_offer in seller_offers:
        book_info = get_book_info(isbn=seller_offer.isbn)["book"]
        result_offers.append({"title":book_info["title"], "price":seller_offer.price, "offer_id":seller_offer.id,
                       "isbn":seller_offer.isbn})
    
    seller_auctions = get_seller_auctions(seller_id=seller_id)
    auctions = {}
    for seller_auction in seller_auctions:
        book_info = get_book_info(isbn=seller_auction.isbn)["book"]
        result_auctions.append({"title":book_info["title"], "current_price":seller_auction.current_price, "auction_id":seller_auction.id,
                       "isbn":seller_auction.isbn, "end_time":seller_auction.end_time})
    
    follow_isbns = get_follow_list(user=user)      
    for isbn in follow_isbns:
        min_offer = {}
        min_auction = {}
        if isbn:
            book_info = get_book(isbn=isbn)
            offers = book_info["offers"]
            auctions = book_info["auctions"]
            if offers:
                min_offer = offers[0]
            if auctions:
                min_auction = auctions[0]
            result_follow.append({"isbn":isbn, "book":book_info["book"], "min_offer":min_offer, "min_auction":min_auction})
        else:
            pass
             
    return render(request,'account_index.html', {"offers":result_offers, "auctions":result_auctions, "follows":result_follow})

def login(request):
    from django_cas.views import login, logout
    
    # for testers    
    httpresp = login(request)
    if request.user.is_authenticated():
        if request.user.username not in testers:
            httperror = render(request,'testers.html')
            logout(request)
            return httperror
    return httpresp
    
    
def forbidden(request):
    '''Default 403 handler'''
    return render(request, "403.html")

def not_found(request):
    ''' Default 404 handler '''
    return render(request, "error_page.html")

def product_index(request):
    '''Display the product page for submission'''
    return render(request, "product_index.html")
