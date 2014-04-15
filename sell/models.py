from django.db import models
from search.models import *
from account.models import *

# put offer in table of offers, and update table of users
def put_offer(offer, isbn):
    # create offer
    new_offer = Offer(isbn=isbn, seller_id = offer['seller_id'], price=offer['price'], course=offer["course"], condition=offer['condition'], description=offer['description'], auction_id=offer['auction_id']) 

    # put in table of offers
    new_offer.save()

    # add offer_id to sell_list of seller
    qset = BookUser.objects.filter(id=offer['seller_id'])
    for seller in qset:
         seller.sell_list = seller.sell_list + ' ' + str(new_offer.id)

    return new_offer.id
