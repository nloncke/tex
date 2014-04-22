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
    import time
    from datetime import datetime
    
    pattern = '%m/%d/%y %H:%M:%S'
    epoch = int(time.mktime(time.strptime(auction['end_time'], pattern)))
    auction['end_time'] = epoch
    new_auction = Auction(**auction)
    new_auction.save()
    return new_auction.id

def get_auction_info(auction_id):
    ''''Get auction info given auction_id
    '''
    qset = Auction.objects.filter(id=auction_id)
    for object in qset:
        auction = { 'seller_id': object.seller_id, 'current_price':object.current_price, 'buy_now_price':object.buy_now_price, 'end_time':object.end_time, 
                 'course':object.course, 'condition':object.condition, 'description':object.description, 'isbn':object.isbn }
        return auction

    return None