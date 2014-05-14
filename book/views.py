from django.shortcuts import render
from django.http import HttpResponse
from search.utils import validate_isbn, convert_to_13

def book_index(request):
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
        isbn = convert_to_13(isbn=isbn)
        if validate_isbn(isbn):
            if action == "follow":
                follow_isbns = get_follow_list(user=user) 
                for follow_isbn in follow_isbns:                   
                    if follow_isbn != isbn:
                        i = i + 1
                if i == len(follow_isbns):
                    follow(user=user, isbn=isbn)
            elif action == "unfollow":
                unfollow(user=user, isbn=isbn) 
            else:
                return render(request, 'error_page.html')
    else:
        isbn = request.GET.get("isbn","0")
        isbn = convert_to_13(isbn=isbn)

    if validate_isbn(isbn=isbn): 
        result = get_book(isbn=isbn)
        follow_isbns = get_follow_list(user=user)  
        for follow_isbn in follow_isbns:
            if follow_isbn:
                if follow_isbn == isbn:
                    result["is_follow"] = "true" 
        return render(request, 'book_index.html', result)      

    return render(request, 'error_page.html')   
    
def add(request):  
    from search.utils import search_by_isbn
    result = {}
    if request.method == 'GET':
        isbn = request.GET.get("isbn","0")
        isbn = isbn.lstrip()
        isbn = isbn.rstrip()
        if validate_isbn(isbn=isbn):
            isbn = re.sub("[^0-9Xx]", "", isbn)
            isbn = convert_to_13(isbn=isbn)
            results = search_by_isbn(isbn)["books"]
            if results:
                return book_index(request)
         
        return render(request, 'search_empty.html', {"query": isbn}) 
    return render(request, "error_page.html")   
          