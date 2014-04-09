from django.shortcuts import render
from sell.forms import SellForm
from search.views import validate_isbn
from search.models import *
result = {}
def sell_form(request):   
    global result
    if request.method == 'POST':
        isbn = request.POST.get("target_isbn","0")
        if validate_isbn(isbn):
            result = get_book_info(isbn, thumb=False)       
            form = SellForm(request.POST)
            if form.is_valid():
               sell_data = form.cleaned_data
               return HttpResponseRedirect('/sell/thanks/')
        else:
            # need an error html page
            return render(request, 'search_empty_prompt.html', {"query": isbn})
    else: 
        pass      
    form = SellForm()
        
    result["form"] = form
    return render(request, 'sell_form.html', result)

def sell_confirm(request):
    if request.method == 'POST':   
            form = SellForm(request.POST)
            if form.is_valid():
                sell_data = form.cleaned_data
                # process the data ??
                return HttpResponseRedirect('/sell/thanks/')
    else:       
        form = SellForm()
        
    result["form"] = form   
    return render(request, 'sell_form.html', result)
    
    
def thanks(request):
    return render(request, 'sell_thanks.html')

