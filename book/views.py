from django.shortcuts import render
from django.http import HttpResponse
from utils import *
import re

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
        return render(request, 'book_index.html', {"query": isbn})
          
def validate_isbn(isbn):
    regex = re.compile("^(((\d-?){9}[0-9Xx])|((97[89](\d-?){9}[0-9])))$")
    if regex.search(isbn):
        # Remove non ISBN digits, then split into an array
        chars = list(str(re.sub("[^0-9Xx]", "", isbn)))
        # Remove the final ISBN digit from `chars`, and assign it to `last`
        last  = chars.pop()  
        if len(chars) == 9:
        # Compute the ISBN-10 check digit
            val = sum((x + 2) * int(y) for x,y in enumerate(reversed(chars)))
            check = 11 - (val % 11)
            if check == 10:
                check = "X"
            elif check == 11:
                check = "0"
        else:
        # Compute the ISBN-13 check digit
            val = sum((x % 2 * 2 + 1) * int(y) for x,y in enumerate(chars))
            check = 10 - (val % 10)
            if check == 10:
                check = "0"    
        if (str(check) == last):
            #print "Valid ISBN"
            return True
        else:
            #print "Invalid ISBN check digit"
            return False
    else:
        #print "Invalid ISBN"
        return False