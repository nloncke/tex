from django.shortcuts import render
from django.http import HttpResponse
from utils import *
from book import utils
import re

def buy_confirmation(request):
    result = {}
    if request.method == "POST":
        result["offer_id"] = request.POST.get("offer_id", "0")
        result["buyer_id"] = request.POST.get("buyer_id", "0")
        isbn = result["offer_id"].isbn
        book = get_book(isbn)
        result["book"] = book
        return render(request, "buy_confirmation.html", result)
