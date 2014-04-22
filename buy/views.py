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
    from models import bid_auction, get_current_price, get_auction_isbn, set_buyer_id
    result = {}
    if request.method == "POST":
        buyer_id = request.user.username
        auction_id = request.POST.get("auction_id", "0")
        current_price = request.POST.get("current_price", "0")
        actual_price = get_current_price(auction_id)
        isbn = get_auction_isbn(auction_id)
        result = get_book(isbn)
        if int(current_price) == actual_price:
            bid = request.POST.get("bid", "0")
            bid_auction(auction_id, new_price(current_price,bid))
            set_buyer_id(auction_id=auction_id, buyer_id=buyer_id)
            result["current_price"] = new_price(current_price,bid)
            result["buyer_id"] = buyer_id
        else:
            result["current_price"] = actual_price
            result["error"] = "true"
        return render(request, 'bid_confirmation.html', result)
    return render(request, 'error_page.html')