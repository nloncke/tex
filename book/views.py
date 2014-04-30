from django.shortcuts import render
from django.http import HttpResponse
from search.utils import validate_isbn

def book_index(request):
    from sell.models import put_auction
    from account.models import get_follow_list
    from utils import get_book
    user = request.user
    result = {}
    i = 0 
    if request.method == "POST":
        from sell.utils import get_book_info    
        from account.models import follow, unfollow
        action = request.POST.get("book_action","")
        isbn = request.POST.get("target_isbn", "0")
        if validate_isbn(isbn):
            if action == "follow":
                follow_isbns = get_follow_list(user=user) 
                for follow_isbn in follow_isbns:                   
                    if follow_isbn != isbn:
                        i = i + 1
                if i == len(follow_isbns):
                    follow(user=user, isbn=isbn)
            elif action == "unfollow":
                unfollow(user=user, isbn=isbn)  #BUGS!!!!!
            else:
                return render(request, 'error_page.html')
    else:
        isbn = request.GET.get("isbn","0")
    
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

         
        
  
    
'''def book_follow(request):   
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
        return render(request, 'error_page.html')'''

'''def book_unfollow(request):
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
        return render(request, 'error_page.html')'''
          