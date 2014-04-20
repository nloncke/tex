from django.shortcuts import render
from django.http import HttpResponse
from utils import *
from search.utils import validate_isbn

# render(request, html template, function that returns dictionary)
# render(-, nicole, jeffrey)


def book_index(request):
    from sell.models import put_auction
    auction = {}
    auction["buyer_id"] = "lauraxu"
    auction["seller_id"] = "lx"
    auction["end_time"] = "time"
    auction["current_price"] = "10"
    auction["buy_now_price"] = "30"
    auction["condition"] = "Like New"   
    auction["description"] = "it's great"
    isbn = request.GET.get("isbn","0")
    auction["isbn"] = isbn
    auction_id = put_auction(auction)
    if validate_isbn(isbn):
        result = get_book(isbn)
        return render(request, 'book_index.html', result)      
    else:
        # need an error html page
        return render(request, 'search_empty_prompt.html', {"query": isbn})
    
    
def book_follow(request):
    result = {}
    from account.models import follow
    isbn = request.POST.get("target_isbn", "0")
    username = request.user.username
    user = request.user
    if validate_isbn(isbn):
        follow(user=user, isbn=isbn)
        result["isbn"] = isbn
        result["user"] = username
        return render(request, 'account_index.html', result)
    else:
        return render(request, 'error_page.html')
        # error page
        
        