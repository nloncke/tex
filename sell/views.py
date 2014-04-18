from django.shortcuts import render
from search.views import validate_isbn
from utils import get_book_info, put_offer
from book.utils import get_book
from django_cas.decorators import login_required
#from buy.models import remove_offer, edit_offer

@login_required
def sell_form(request):   
    result = {}
    if request.method == 'POST':
        isbn = request.POST.get("target_isbn","0")
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
       
@login_required
def sell_submit(request):
    offer = {}
    result = {}
    if request.method == 'POST':   
        offer["isbn"] = request.POST.get("target_isbn", "0")
        offer["course"] = request.POST.get("course", "0")
        offer["price"] = request.POST.get("price", "0")
        offer["condition"] = request.POST.get("picked_condition", "0")
        offer["description"] = request.POST.get("description", "0")
        offer["seller_id"] = request.user.username
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

@login_required    
def sell_edit(request):
    from sell.models import get_offer_info
    result = {}
    if request.method == 'POST':  
        offerid = request.POST.get("offer_id", "0")
        offer = get_offer_info(offerid)
        isbn = offer["isbn"]
        result = get_book_info(isbn)
        result["offer"] = offer 
        result["offer_id"] = offerid
    return render(request, "sell_form_edit.html", result)

@login_required
def sell_edit_submit(request):
    from buy.models import edit_offer
    result = {}
    if request.method == 'POST':
        offer_id = request.POST.get("offer_id", "0")
        price = request.POST.get("price" , "0")
        course = request.POST.get("course", "0")
        condition = request.POST.get("picked_condition", "0")
        description = request.POST.get("description", "0")
        edit_offer(offer_id, price, course, condition, description)
        result["offer_id"] = offer_id
        return render(request, 'sell_submit.html', result)      
        
def validate_offer(offer):
    if offer["price"] == "0"|offer["condition"] == "0"|offer["description"] == "0"|offer["seller_id"] == "0":
        return False
    else:
        return True