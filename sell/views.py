from django.shortcuts import render
from search.views import validate_isbn
from utils import *
def sell_form(request):   
    if request.method == 'POST':
        isbn = request.POST.get("target_isbn","0")
        if validate_isbn(isbn):
            result = get_book_info(isbn)       
        else:
            # need an error html page
            return render(request, 'search_empty_prompt.html', {"query": isbn})
    else: 
        pass      
    
    return render(request, 'sell_form.html', result)
       
def sell_submit(request):
    offer = {}
    if request.method == 'POST':   
        offer["price"] = request.POST.get("price", "0")
        offer["picked_condition"] = request.POST.get("picked_condition", "0")
        offer["description"] = request.POST.get("description", "0")
        offer["seller_id"] = "TEMP"
        offer["auction_id"] = "0"
        '''if validate_offer(offer):
            return render(request, 'sell_submit.html')
        else:
            # need an error html page
            return render(request, 'search_empty_prompt.html', {"query": "temporary"})'''
        return render(request, 'sell_submit.html')

def validate_offer(offer):
    if offer.price == "0"|offer.picked_condition == "0"|offer.description == "0"|offer.seller_id == "0":
        return False
    else:
        return True