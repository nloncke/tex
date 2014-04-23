from django.shortcuts import render
from django.http import HttpResponse
from utils import *
from models import *
from book.utils import *


def buy_confirmation(request):
    result = {}
    if request.method == "POST":
        is_auction = request.POST.get("is_auction","")
        if is_auction:
            from models import remove_auction
            result = {}
            if request.method == "POST":
                auction_id = request.POST.get("auction_id","0")
                buyer_id = request.user.username
                sold_auction = remove_auction(auction_id, True)
                if sold_auction:
                    isbn = sold_auction["isbn"]
                    seller_id = sold_auction["seller_id"]
                    result = get_book(isbn)
                    result["sold_offer"] = sold_auction
                    result["seller_id"] = seller_id
        else:
            offer_id = request.POST.get("offer_id", "0")
            buyer_id = request.user.username
            sold_offer = remove_offer(offer_id)
            if sold_offer:
                isbn = sold_offer["isbn"]
                seller_id = sold_offer["seller_id"]
                result = get_book(isbn)
                result["sold_offer"] = sold_offer
                result["seller_id"] = seller_id
        return render(request, "buy_confirmation.html", result)
    return render(request, 'error_page.html')

def bid(request):
    from models import bid_auction, get_auction_isbn
    result = {}
    if request.method == "POST":
        buyer_id = request.user.username
        auction_id = request.POST.get("auction_id", "0")
        current_price = request.POST.get("current_price", "0")
        
        # Try to bid in one atomic action
        bid = request.POST.get("bid", "0")
        new_bid = int(current_price) + int(bid)
        new_current_price = bid_auction(auction_id, new_bid, buyer_id)
        
        isbn = get_auction_isbn(auction_id)
        result = get_book(isbn)
        
        result["current_price"] = new_current_price
        
        if int(new_current_price) == new_bid:
            result["buyer_id"] = buyer_id
        else:
            result["error"] = "true"
        return render(request, 'bid_confirmation.html', result)
    
    return render(request, 'error_page.html')