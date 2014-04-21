from django.shortcuts import render
from search.views import validate_isbn
from utils import get_book_info, put_offer, validate_offer
from book.utils import get_book
#from buy.models import remove_offer, edit_offer

def sell_form(request):   
    result = {}
    if request.method == 'GET':
        isbn = request.GET.get("isbn","0")
        if validate_isbn(isbn):
            result = get_book_info(isbn)
            return render(request, 'sell_form.html', result)    
        else:
            # need an error html page
            return render(request, 'search_empty_prompt.html', {"query": isbn})
    else: 
        # Show error page
        #return render(request, "error_page.html")      
        pass   
       
def sell_submit(request):
    from sell.models import put_auction
    offer = {}
    result = {}
    if request.method == 'POST':  
        is_auction = request.POST.get("is_auction", "0")
        if is_auction == "yes":
            offer["isbn"] = request.POST.get("target_isbn", "0")
            offer["course"] = request.POST.get("course", "0")
            offer["buy_now_price"] = request.POST.get("price", "0")
            offer["condition"] = request.POST.get("picked_condition", "0")
            offer["description"] = request.POST.get("description", "0")
            offer["seller_id"] = request.user.username
            offer["buyer_id"] = ""
            offer["current_price"] = 10
            offer["end_time"] = request.POST.get("end_time", "0")
            result["offer_id"] = put_auction(offer)
            result["is_auction"] = "true"
        else:
            offer["isbn"] = request.POST.get("target_isbn", "0")
            offer["course"] = request.POST.get("course", "0")
            offer["price"] = request.POST.get("price", "0")
            offer["condition"] = request.POST.get("picked_condition", "0")
            offer["description"] = request.POST.get("description", "0")
            offer["seller_id"] = request.user.username
            result["offer_id"] = put_offer(offer)
            #result["is_auction"] = "false"offer
        
        return render(request, 'sell_submit.html', result)
       
        
        '''if validate_offer(offer) and validate_isbn(isbn):
            put_offer(offer)
            return render(request, 'sell_submit.html')
        else:
            # need an error html page
            return render(request, 'search_empty_prompt.html', {"query": "temporary"})'''
        
        
    else:
        return render(request, "error_page.html")

  
def sell_edit(request):
    from sell.models import get_offer_info, get_auction_info
    result = {}
    if request.method == 'POST':  
        is_auction = request.POST.get("is_auction", "")
        offerid = request.POST.get("offer_id", "0")
        if is_auction:
            offer = get_auction_info(offerid)
        else:
            offer = get_offer_info(offerid)
        isbn = offer["isbn"]
        result = get_book_info(isbn)
        result["offer"] = offer 
        result["offer_id"] = offerid
        result["is_auction"] = is_auction
    return render(request, "sell_form_edit.html", result)


def sell_edit_submit(request):
    from buy.models import edit_offer, edit_auction
    result = {}
    if request.method == 'POST':
        is_auction = request.POST.get("is_auction", "")
        offer_id = request.POST.get("offer_id", "0")
        course = request.POST.get("course", "0")
        condition = request.POST.get("picked_condition", "0")
        description = request.POST.get("description", "0")
        if is_auction:
            auction_id=offer_id
            edit_auction(auction_id, course, condition, description)
        else:
            price = request.POST.get("price" , "0")
            edit_offer(offer_id, price, course, condition, description)
            
        result["offer_id"] = offer_id
        result["is_auction"] = is_auction
        return render(request, 'sell_submit.html', result)      