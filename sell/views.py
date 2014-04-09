from django.shortcuts import render
from search.views import validate_isbn
from utils import *
def sell_form(request):   
    if request.method == 'POST':
        isbn = request.POST.get("target_isbn","0")
        if validate_isbn(isbn):
            result = get_book_info(isbn)       
        else:
            # need an error html page
            return render(request, 'search_empty_prompt.html', {"query": isbn})
    else: 
        pass      
    
    return render(request, 'sell_form.html', result)
       
def sell_submit(request):
    return render(request, 'sell_submit.html')

