from django.shortcuts import render
from django.http import HttpResponse
from utils import *
import re
from search.views import validate_isbn

# render(request, html template, function that returns dictionary)
# render(-, nicole, jeffrey)

def book_index(request):
    auction = {}
    auction["auction_id"] = "5"
    auction["last_price"] = "20"
    auction["buy_now_price"] = "30"
    auction["condition"] = "Like New"
    auction["description"] = "it's great"
    isbn = request.POST.get("target_isbn","0")
    if validate_isbn(isbn):
        result = get_book(isbn)
        result["auction"] = auction
        return render(request, 'book_index.html', result)      
    else:
        # need an error html page
        return render(request, 'search_empty_prompt.html', {"query": isbn})
    
def book_follow(request):
    isbn = request.POST.get("target_isbn", "0")
    follow_user_id = request.POST.get("follow_user_id", "0")
    if validate_isbn(isbn):
        add_to_follow(follow_user_id=follow_user_id, isbn=isbn)
        result["isbn"] = isbn
        result["follow_user_id"] = follow_user_id
        return render(request, 'account_index', result)
    
    else:
        pass
        # error page
        
        