from django.shortcuts import render
from sell.forms import SellForm

def sell_form(request):
    if request.method == 'POST':
        form = SellForm(request.POST)
        if form.is_valid():
            sell_data = form.cleaned_data
            # process the data ??
            return HttpResponseRedirect('/sell/thanks/')
    else:
        form = SellForm()
    return render(request, 'sell_index_lx.html', {'form': form})
    
def thanks(request):
    return render(request, 'sell_thanks.html')

