from django.shortcuts import render
from django.http import HttpResponse
from utils import *
from search.utils import validate_isbn

# render(request, html template, function that returns dictionary)
# render(-, nicole, jeffrey)


def book_index(request):
    from sell.models import put_auction
    from account.models import get_follow_list
    isbn = request.GET.get("isbn","0")
    user = request.user
    if validate_isbn(isbn):
        result = get_book(isbn)
        follow_isbns = get_follow_list(user=user)  
        for follow_isbn in follow_isbns:
            if follow_isbn:
                if follow_isbn == isbn:
                    result["is_follow"] = "true" 
        return render(request, 'book_index.html', result)      
    else:
        return render(request, 'search_empty_prompt.html', {"query": isbn})
    
  
    
def book_follow(request):
    from sell.utils import get_book_info
    result = {}
    from account.models import follow
    isbn = request.POST.get("target_isbn", "0")
    username = request.user.username
    user = request.user
    if validate_isbn(isbn):
        follow(user=user, isbn=isbn)
        result = get_book_info(isbn)
        return render(request, 'follow_unfollow_confirmation.html', result) # need to reload page or something else
    else:
        return render(request, 'error_page.html')
        # error page

def book_unfollow(request):
    from account.models import unfollow
    from search.utils import validate_isbn
    from sell.utils import get_book_info
    result = {}
    if request.method == "POST":   
        isbn = request.POST.get("target_isbn", "0")
        user = request.user
        if validate_isbn(isbn):
            result = get_book_info(isbn)
            unfollow(user=user, isbn=isbn)  
            result["is_unfollow"] = "true"
            return render(request, 'follow_unfollow_confirmation.html', result) 
    else:
        return render(request, 'error_page.html')
    
          