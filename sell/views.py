from django.shortcuts import render
from search.utils import validate_isbn, convert_to_13
import re

def sell_form(request):   
    from search.utils import search_by_isbn
    from book.utils import add_links
    result = {}
    if request.method == 'GET':
        isbn = request.GET.get("isbn","0")
        isbn = isbn.lstrip()
        isbn = isbn.rstrip()
        if validate_isbn(isbn=isbn):
            isbn = re.sub("[^0-9Xx]", "", isbn)
            isbn = convert_to_13(isbn=isbn)
            results = search_by_isbn(query=isbn, thumb=False)["books"]
            if results:
                result["book"] = results[0]
                add_links(result["book"])
                return render(request, 'sell_form.html', result)
        return render(request, 'search_empty.html', {"query": isbn})
    return render(request, "error_page.html")   
       
def sell_submit(request):
    from utils import put_offer, put_auction
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
            offer["current_price"] = request.POST.get("current_price","0")
            offer["end_time"] = request.POST.get("end_time", "0")
            result["offer_id"] = put_auction(auction=offer)
            result["is_auction"] = "true"
            result["isbn"] = offer["isbn"]
        else:
            offer["isbn"] = request.POST.get("target_isbn", "0")
            offer["course"] = request.POST.get("course", "0")
            offer["price"] = request.POST.get("price", "0")
            offer["condition"] = request.POST.get("picked_condition", "0")
            offer["description"] = request.POST.get("description", "0")
            offer["seller_id"] = request.user.username
            result["offer_id"] = put_offer(offer=offer)
            result["isbn"] = offer["isbn"]
    
        return render(request, 'sell_submit.html', result)                
    else:
        return render(request, "error_page.html")

def sell_edit(request):
    from sell.models import get_offer_info, get_auction_info
    from utils import get_book_info
    from book.utils import add_links
    result = {}
    if request.method == 'POST':  
        is_auction = request.POST.get("is_auction", "")
        offerid = request.POST.get("offer_id", "0")
        if is_auction:
            offer = get_auction_info(auction_id=offerid)
        else:
            offer = get_offer_info(offer_id=offerid)
        isbn = offer["isbn"]
        result = get_book_info(isbn=isbn)
        add_links(result["book"])
        result["offer"] = offer 
        result["offer_id"] = offerid
        result["is_auction"] = is_auction
        return render(request, "sell_form_edit.html", result)
    else:
        return render(request, "error_page.html")  

def sell_edit_submit(request):
    from buy.models import edit_offer, edit_auction
    result = {}
    if request.method == 'POST':
        isbn = request.POST.get("target_isbn", "0")
        if validate_isbn(isbn=isbn):
            is_auction = request.POST.get("is_auction", "")
            offer_id = request.POST.get("offer_id", "0")
            course = request.POST.get("course", "0")
            condition = request.POST.get("picked_condition", "0")
            description = request.POST.get("description", "0")
            if is_auction:
                auction_id=offer_id
                edit_auction(auction_id=auction_id, course=course, condition=condition, description=description)
            else:
                price = request.POST.get("price" , "0")
                edit_offer(offer_id=offer_id, price=price, course=course, condition=condition, description=description)
                
            result["offer_id"] = offer_id
            result["is_auction"] = is_auction
            result["isbn"] = isbn
            return render(request, 'sell_submit.html', result) 
        else:
            return render(request, "error_page.html")     
    else:
        return render(request, "error_page.html")  