from django.shortcuts import render
from sell.forms import SellForm
from search.views import validate_isbn
from book.utils import *

def sell_form(request):
    book = []
    if request.method == 'POST':
        isbn = request.POST.get("target_isbn","0")
        if validate_isbn(isbn):
            book = get_book(isbn)       
            form = SellForm(request.POST)
            if form.is_valid():
                sell_data = form.cleaned_data
                # process the data ??
                return HttpResponseRedirect('/sell/thanks/')
        else:
            # need an error html page
            return render(request, 'search_empty_prompt.html', {"query": isbn})
    else:       
        form = SellForm()
        
    return render(request, 'sell_index_lx.html', {'form': form,'book':book})
    
def thanks(request):
    return render(request, 'sell_thanks.html')

