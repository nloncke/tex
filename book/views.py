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