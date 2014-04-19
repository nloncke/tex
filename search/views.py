from django.shortcuts import render
from django.http import HttpResponse
from utils import *
import re

# render(request, html template, function that returns dictionary)
# render(-, nicole, jeffrey)
def index(request):
    return render(request,'index.html')

def isbn(request):
    # change to isbn13
    isbn = request.POST.get("search_input","0")
    isbn = isbn.lstrip()
    isbn = isbn.rstrip()
    if validate_isbn(isbn):
        isbn = re.sub("[^0-9Xx]", "", isbn)
        isbn = convert_to_13(isbn)
        books = search_by_isbn(isbn)
        if books["books"]:
            books["query"] = isbn
            return render(request, 'search_results.html', books)
        else:
            return render(request, 'search_empty.html', {"query": isbn})
    else:
        return render(request, 'search_empty.html', {"query": isbn})
    
def title(request):
    title = request.POST.get("search_input","0")
    title = title.lstrip()
    title = title.rstrip()
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
    author = author.lstrip()
    author = author.rstrip()
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
    course = course.lstrip()
    course = course.rstrip()
    if validate_course(course):
        books = search_by_course(course)
        if books["books"]:
            books["query"] = course
            return render(request, 'search_results.html', books)
        else:
            return render(request, 'search_empty_prompt.html', {"query": course})
    else:
        return render(request, 'search_empty_prompt.html', {"query": course})
        

        
##########################################################  

# For error page
def error_page(request):
    return render(request, "error_page.html")  
