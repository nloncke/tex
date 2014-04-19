from django.db import models
from search.models import *
from account.models import *

def put_offer(offer):
    '''Put offer in table of offers, and update table of users
    '''
    # create offer
    new_offer = Offer(**offer) 

    # put in table of offers
    new_offer.save()

    return new_offer.id

def get_offer_info(offer_id):
    # get info of offer with given id
    # FILTER
    qset = Offer.objects.filter(id=offer_id)
    for object in qset:
        offer = { 'seller_id': object.seller_id, 'price':object.price, 'course':object.course, 'condition':object.condition, 'description':object.description, 'isbn':object.isbn }
        return offer

    return None

def put_auction(auction):
    '''Put an auction in table of auctions, and update table of users
    '''
    return 0
