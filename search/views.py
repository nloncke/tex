from django.shortcuts import render
from django.http import HttpResponse
import re

# render(request, html template, function that returns dictionary)
# render(-, nicole, jeffrey)
def index(request):
    return render(request,'index.html')

def isbn(request):
    from utils import search_by_isbn, validate_isbn, convert_to_13
    if request.method == "POST":
        isbn = request.POST.get("search_input","0")
        isbn = isbn.lstrip()
        isbn = isbn.rstrip()
        if validate_isbn(isbn=isbn):
            isbn = re.sub("[^0-9Xx]", "", isbn)
            isbn = convert_to_13(isbn=isbn)
            books = search_by_isbn(query=isbn)
            if books["books"]:
                books["query"] = isbn
                return render(request, 'search_results.html', books)
            else:
                return render(request, 'search_empty.html', {"query": isbn})
        else:
            return render(request, 'search_empty.html', {"query": isbn})
    else:
        return render(request, "error_page.html")  
    
def title(request):
    from utils import search_by_title, validate_title
    if request.method == "POST":
        title = request.POST.get("search_input","0")
        title = title.lstrip()
        title = title.rstrip()
        if validate_title(title=title):
            books = search_by_title(query=title)
            if books["books"]:
                books["query"] = title
                books["search_length"] = len(books["books"])
                return render(request, 'search_results.html', books)
            else:
                return render(request, 'search_empty_prompt.html', {"query": title})
        else:
            return render(request, 'search_empty_prompt.html', {"query": title})

def author(request):
    from utils import search_by_author, validate_author
    if request.method == "POST":
        author = request.POST.get("search_input","0")
        author = author.lstrip()
        author = author.rstrip()
        if validate_author(author=author):
            books = search_by_author(query=author)
            if books["books"]:
                books["query"] = author
                return render(request, 'search_results.html', books)
            else:
                return render(request, 'search_empty_prompt.html', {"query": author})
        else:
            return render(request, 'search_empty_prompt.html', {"query": author})
    else:
        return render(request, "error_page.html")  
    
def course(request):
    from utils import search_by_course, validate_course
    if request.method == "POST":
        course = request.POST.get("search_input","0")
        course = course.lstrip()
        course = course.rstrip()
        if validate_course(course=course):
            books = search_by_course(query=course)
            if books["books"]:
                books["query"] = course
                return render(request, 'search_results.html', books)
            else:
                return render(request, 'search_empty_prompt.html', {"query": course})
        else:
            return render(request, 'search_empty_prompt.html', {"query": course})
    else:
        return render(request, "error_page.html")      

        
##########################################################  

# For error page
def error_page(request):
    return render(request, "error_page.html")  
