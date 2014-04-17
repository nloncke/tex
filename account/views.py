from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.template import RequestContext, loader
from utils import *
import re

# render(request, html template, function that returns dictionary)
# render(-, nicole, jeffrey)
def account_index(request):
    from account.models import get_seller_offers
    from sell.utils import get_book_info
    result = []
    seller_id = 10
    seller_offers = get_seller_offers(seller_id)
    offers = {}
    for seller_offer in seller_offers:
        book_info = get_book_info(seller_offer.isbn)["book"]
        #offers["offer"] = {"title":book_info["title"], "price":seller_offer.price, "offer_id":seller_offer.offer_id}
        result.append({"title":book_info["title"], "price":seller_offer.price})
    return render(request,'account_index.html', {"offers":result})


def forbidden(request, template_name='403.html'):
    """Default 403 handler"""

    t = loader.get_template(template_name)
    return HttpResponseForbidden(t.render(RequestContext(request)))
