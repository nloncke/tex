from django.shortcuts import render
from django.http import HttpResponse
from utils import *
from models import *
from book.utils import *


def buy_confirmation(request):
    result = {}
    if request.method == "POST":
        offer_id = request.POST.get("offer_id", "0")
        buyer_id = request.user.username
        sold_offer = remove_offer(offer_id)
        if sold_offer:
            isbn = sold_offer["isbn"]
            seller_id = sold_offer["seller_id"]
            result = get_book(isbn)
            result["sold_offer"] = sold_offer
            result["seller_id"] = seller_id
        return render(request, "buy_confirmation.html", result)
    return render(request, 'error_page.html')

