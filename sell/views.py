from django.shortcuts import render
from search.views import validate_isbn
from utils import *
from book.utils import *
from buy.models import *

def sell_form(request):   
    result = {}
    if request.method == 'POST':
        isbn = request.POST.get("target_isbn","0")
        if validate_isbn(isbn):
            result["book"] = get_book_info(isbn)[0]
            return render(request, 'sell_form.html', result)    
        else:
            # need an error html page
            return render(request, 'search_empty_prompt.html', {"query": isbn})
    else: 
        # Show error page
        #return render(request, "error_page.html")      
        pass
    
       
def sell_submit(request):
    offer = {}
    result = {}
    if request.method == 'POST':   
        offer["isbn"] = request.POST.get("target_isbn", "0")
        offer["course"] = request.POST.get("course", "0")
        offer["price"] = request.POST.get("price", "0")
        offer["condition"] = request.POST.get("picked_condition", "0")
        offer["description"] = request.POST.get("description", "0")
        offer["seller_id"] = 10
        offer["auction_id"] = "0"
        result["offer_id"] = put_offer(offer["isbn"], offer)
        '''if validate_offer(offer) and validate_isbn(isbn):
            put_offer(offer)
            return render(request, 'sell_submit.html')
        else:
            # need an error html page
            return render(request, 'search_empty_prompt.html', {"query": "temporary"})'''
        return render(request, 'sell_submit.html', result)
    else:
        return render(request, "error_page.html")
    
def sell_edit(request):
    result = {}
    if request.method == 'POST':  
        offerid = request.POST.get("offer_id", "0")
        edit_offer = get_offer(offerid)
        book_isbn = edit_offer["isbn"]
        result["offer"] = get_book(book_isbn)       
    return render(request, "sell_form_edit.html", result)

def validate_offer(offer):
    if offer["price"] == "0"|offer["condition"] == "0"|offer["description"] == "0"|offer["seller_id"] == "0":
        return False
    else:
        return True