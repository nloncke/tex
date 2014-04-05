from django.shortcuts import render
from django.http import HttpResponse
from utils import *
from django.shortcuts import render_to_response
import re

# render(request, html template, function that returns dictionary)
# render(-, nicole, jeffrey)
def index(request):
    return render(request,'index.html')

def isbn(request):
    isbn = request.POST.get("search_input","0")
    if validate_isbn(isbn):
        books = search_by_isbn(isbn)
        if books["books"]:
            books["isbn"] = isbn
            return render(request, 'search_results.html', books)
        else:
            return render(request, 'search_empty.html', {"isbn": isbn})
    else:
        return render(request, 'search_empty.html', {"isbn": isbn})
    
def title(request):
    title = request.POST.get("search_input","0")
    if validate_title(title):
        books = search_by_title(title)
        if books["books"]:
            books["query"] = title
            return render(request, 'search_results.html', books)
        else:
            return render(request, 'search_empty_prompt.html', {"query": title})
    else:
        return render(request, 'search_empty_prompt.html', {"query": title})

def author(request):
    author = request.POST.get("search_input","0")
    if validate_author(author):
        books = search_by_author(author)
        if books["books"]:
            books["query"] = author
            return render(request, 'search_results.html', books)
        else:
            return render(request, 'search_empty_prompt.html', {"query": author})
    else:
        return render(request, 'search_empty_prompt.html', {"query": author})
    
def course(request):
    course = request.POST.get("search_input","0")
    if validate_course(course):
        books = search_by_course(course)
        if books["books"]:
            books["query"] = course
            return render(request, 'search_results.html', books)
        else:
            return render(request, 'search_empty_prompt.html', {"query": course})
    else:
        return render(request, 'search_empty_prompt.html', {"query": course})
        
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

def validate_title(title):
    regex = re.compile("^[\w\s]{1,200}$")
    if re.search(regex, title):
        return True
    else:
        return False
        
def validate_author(author):
    regex = re.compile("^[a-zA-Z\s]{1,100}$")
    if re.search(regex, author):
        return True
    else:
        return False

def validate_course(course):
    regex = re.compile("[a-zA-Z]{3}( )*[0-9]{3}$")
    if re.search(regex, course):
        return True
    else:
        return False
        
def convert_to_13(isbn):
    if len(isbn) == 13:
        return isbn
    if len(isbn) == 10:
        chars = ['9', '7', '8']
        chars = chars + isbn
        val = sum((x % 2 * 2 + 1) * int(y) for x,y in enumerate(chars))
        check = 10 - (val % 10)
        if check == 10:
            check = "0"
        chars.append(str(check))
        return ''.join(chars)
    else:
        print "Conversion requires ISBN-10"
        
##########################################################    
