from django.shortcuts import render
from django.http import HttpResponse

def buy_confirmation(request):
    from book.utils import get_book
    from utils import notify_users_bought
    from models import remove_offer
    result = {}
    if request.method == "POST":
        is_auction = request.POST.get("is_auction","")
        if is_auction:
            from models import remove_auction
            result = {}
            auction_id = request.POST.get("auction_id","0")
            buyer_id = request.user.username
            sold_auction = remove_auction(auction_id, True, buyer_id=buyer_id)
            if sold_auction:
                isbn = sold_auction["isbn"]
                seller_id = sold_auction["seller_id"]
                result = get_book(isbn=isbn)
                result["sold_offer"] = sold_auction
                result["seller_id"] = seller_id
                notify_users_bought(buyer=buyer_id, offer=sold_auction)      
            if sold_auction == None:
                return render(request, 'nocheating.html', {'buyer_id':buyer_id, 'error':"cheating"})         
        else:
            offer_id = request.POST.get("offer_id", "0")
            buyer_id = request.user.username
            sold_offer = remove_offer(offer_id, buyer_id=buyer_id)
            if sold_offer == None:
                return render(request, 'nocheating.html', {'buyer_id':buyer_id, 'error':"cheating"})
            if sold_offer:
                isbn = sold_offer["isbn"]
                seller_id = sold_offer["seller_id"]
                result = get_book(isbn=isbn)
                result["sold_offer"] = sold_offer
                result["seller_id"] = seller_id
                notify_users_bought(buyer=buyer_id, offer=sold_offer)
        return render(request, "buy_confirmation.html", result)
    
    return render(request, 'error_page.html')

def bid(request):
    from models import bid_auction, get_auction_isbn
    from search.utils import get_book_info
    from utils import notify_old_bidder
    result = {}
    if request.method == "POST":
        buyer_id = request.user.username
        auction_id = request.POST.get("auction_id", "0")
        current_price = request.POST.get("current_price", "0")
        
        # Try to bid in one atomic action
        bid = request.POST.get("bid", "0")
        new_bid = int(current_price) + int(bid)
        (new_current_price, old_buyer, info) = bid_auction(auction_id=auction_id, current_price=new_bid, buyer_id=buyer_id)
        if new_current_price == 1:
            return render(request, 'nocheating.html', {'buyer_id':buyer_id, 'error':"cheating"})
        if new_current_price == 2:
            return render(request, 'nocheating.html', {'buyer_id':buyer_id})

        isbn = info["isbn"]
        
        result = get_book_info(isbn=isbn, thumb=False)[0]
    
        result["current_price"] = str(new_current_price)
        result["end_time"] = info["end_time"]

        if old_buyer:
            notify_old_bidder(old_buyer, result)
        
        if new_current_price == new_bid:
            result["buyer_id"] = buyer_id
        else:
            result["error"] = "true"
        return render(request, 'bid_confirmation.html', result)
    
    return render(request, 'error_page.html')