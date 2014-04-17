from django.shortcuts import render
from django.http import HttpResponse
from django_cas.decorators import login_required
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
    
    
@login_required
def book_follow(request):
    from account.models import follow
    isbn = request.POST.get("target_isbn", "0")
    user = request.user.username
    if validate_isbn(isbn):
        follow(user=user, isbn=isbn)
        result["isbn"] = isbn
        result["user"] = user
        return render(request, 'account_index', result)
    else:
        pass
        # error page
        
        