from django.shortcuts import render
from django.http import HttpResponse
from utils import *
import re
from search.views import validate_isbn

# render(request, html template, function that returns dictionary)
# render(-, nicole, jeffrey)

def book_index(request):
    # change to isbn13
    isbn = request.POST.get("target_isbn","0")
    if validate_isbn(isbn):
        book = get_book(isbn)
        return render(request, 'book_index.html', book)      
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
        
        