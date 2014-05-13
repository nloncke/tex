from django.shortcuts import render
from django.http import HttpResponse
import re

def index(request):
    return render(request,'index.html')

def isbn(request):
    from utils import search_by_isbn, validate_isbn, convert_to_13
    from search.models import get_offers, get_auctions
    if request.method == "POST":
        isbn = request.POST.get("search_input","0")
        isbn = isbn.lstrip()
        isbn = isbn.rstrip()
        if validate_isbn(isbn=isbn):
            isbn = re.sub("[^0-9Xx]", "", isbn)
            isbn = convert_to_13(isbn=isbn)
            result = search_by_isbn(query=isbn)
            if result["books"]:
                result["query"] = isbn
                result["search_length"] = len(result["books"])
                for book in result["books"]:
                    offer = sorted(get_offers(book["isbn"]), key=(lambda x:x["buy_price"]))
                    if offer:
                        book["min_offer"] = offer[0]["buy_price"]
                    auction = sorted(get_auctions(book["isbn"]), key=(lambda y:y["current_price"])) 
                    if auction:
                        book["min_auction"] = auction[0]["current_price"]
                
                return render(request, 'search_results.html', result)
            else:
                return render(request, 'search_empty.html', {"query": isbn})
        else:
            return render(request, 'search_empty.html', {"query": isbn})
    return render(request, 'error_page.html')    
    
def title(request):
    from utils import search_by_title
    from search.models import get_offers, get_auctions
    if request.method == "POST":
        title = request.POST.get("search_input","0")
        title = title.lstrip()
        title = title.rstrip()
        result = search_by_title(query=title)
        if result["books"]:
            result["query"] = title
            result["search_length"] = len(result["books"])
            for book in result["books"]:
                offer = sorted(get_offers(book["isbn"]), key=(lambda x:x["buy_price"]))
                if offer:
                    book["min_offer"] = offer[0]["buy_price"]
                auction = sorted(get_auctions(book["isbn"]), key=(lambda y:y["current_price"])) 
                if auction:
                    book["min_auction"] = auction[0]["current_price"]
            
            return render(request, 'search_results.html', result)
        else:
            return render(request, 'search_empty_prompt.html', {"query": title})
    return render(request, 'error_page.html')    

def author(request):
    from utils import search_by_author
    from search.models import get_offers, get_auctions
    if request.method == "POST":
        author = request.POST.get("search_input","0")
        author = author.lstrip()
        author = author.rstrip()
        result = search_by_author(query=author)
        if result["books"]:
            result["query"] = author
            result["search_length"] = len(result["books"])
            for book in result["books"]:
                offer = sorted(get_offers(book["isbn"]), key=(lambda x:x["buy_price"]))
                if offer:
                    book["min_offer"] = offer[0]["buy_price"]
                auction = sorted(get_auctions(book["isbn"]), key=(lambda y:y["current_price"])) 
                if auction:
                    book["min_auction"] = auction[0]["current_price"]
            
            return render(request, 'search_results.html', result)
        else:
            return render(request, 'search_empty_prompt.html', {"query": author})
    return render(request, 'error_page.html')      
    
def course(request):
    from utils import search_by_course, validate_course
    from search.models import get_offers, get_auctions
    if request.method == "POST":
        course = request.POST.get("search_input","0")
        course = course.lstrip()
        course = course.rstrip()
        if validate_course(course=course):
            result = search_by_course(query=course)
            if result["books"]:
                result["query"] = course
                result["search_length"] = len(result["books"])
                for book in result["books"]:
                    offer = sorted(get_offers(book["isbn"]), key=(lambda x:x["buy_price"]))
                    if offer:
                        book["min_offer"] = offer[0]["buy_price"]
                    auction = sorted(get_auctions(book["isbn"]), key=(lambda y:y["current_price"])) 
                    if auction:
                        book["min_auction"] = auction[0]["current_price"]
                
                return render(request, 'search_results.html', result)
            else:
                return render(request, 'search_empty_prompt.html', {"query": course})
        else:
            return render(request, 'search_empty_prompt.html', {"query": course})
    return render(request, 'error_page.html')       

        
##########################################################  

# For error page
def error_page(request):
    return render(request, "error_page.html")  
