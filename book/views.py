from django.shortcuts import render
from django.http import HttpResponse
from search.utils import validate_isbn, convert_to_13

def book_index(request):
    from account.models import get_follow_list
    from utils import get_book
    if request.method == "GET":
        isbn = request.GET.get("isbn","0")
        isbn = convert_to_13(isbn=isbn)
        user = request.user
        if validate_isbn(isbn=isbn):
            result = get_book(isbn=isbn)
            follow_isbns = get_follow_list(user=user)  
            for follow_isbn in follow_isbns:
                if follow_isbn:
                    if follow_isbn == isbn:
                        result["is_follow"] = "true" 
            return render(request, 'book_index.html', result)      
        else:
            return render(request, 'error_page.html')
    else:
        return render(request, 'error_page.html')
  
    
def book_follow(request):   
    from sell.utils import get_book_info    
    from account.models import follow
    result = {}
    if request.method == "POST":
        isbn = request.POST.get("target_isbn", "0")
        username = request.user.username
        user = request.user
        if validate_isbn(isbn):
            follow(user=user, isbn=isbn)
            result = get_book_info(isbn=isbn)
            return render(request, 'follow_unfollow_confirmation.html', result) # need to reload page or something else
        else:
            return render(request, 'error_page.html')
    else:
        return render(request, 'error_page.html')

def book_unfollow(request):
    from account.models import unfollow
    from sell.utils import get_book_info
    result = {}
    if request.method == "POST":   
        isbn = request.POST.get("target_isbn", "0")
        user = request.user
        if validate_isbn(isbn=isbn):
            result = get_book_info(isbn=isbn)
            unfollow(user=user, isbn=isbn)  
            result["is_unfollow"] = "true"
            return render(request, 'follow_unfollow_confirmation.html', result) 
    else:
        return render(request, 'error_page.html')
    
    
def add(request):  
    from search.utils import search_by_isbn
    result = {}
    if request.method == 'GET':
        isbn = request.GET.get("isbn","0")
        if validate_isbn(isbn=isbn):
            isbn = convert_to_13(isbn=isbn)
            results = search_by_isbn(isbn)["books"]
            if results:
                return book_index(request)
         
        return render(request, 'search_empty.html', {"query": isbn}) 
    return render(request, "error_page.html")   
    
          