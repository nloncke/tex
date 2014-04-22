from django.shortcuts import render
from django.http import HttpResponse
from utils import *
from search.utils import validate_isbn

# render(request, html template, function that returns dictionary)
# render(-, nicole, jeffrey)


def book_index(request):
    from sell.models import put_auction
    isbn = request.GET.get("isbn","0")
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
        
        