from search.models import *
from account.models import *
import time

def remove_offer(offer_id):
    '''
    Returns the isbn, seller id and price of the given offer
    Also deletes it from database
    '''
    qset = Offer.objects.filter(id=offer_id)
    if len(qset) > 0:
        d =  { 'isbn': qset[0].isbn, 'seller_id':qset[0].seller_id, 'price':qset[0].price }
        qset[0].delete()
        return d

    else:
        return {}
    
    
def remove_auction(auction_id, buy_now=False):
    '''
    Returns the isbn, seller id, bidder_id and current_price of the given auction   
    If buy_now, return buy_now_price. 
    Also deletes it from database
    '''
    return {}

def expired_auctions():
        '''
        Returns a list of auction objects corresponding to the auctions that have expired.
        Also deletes the auction objects from the database. 
        '''
        qset = Auction.objects.filter(end_time__lt=time.time())
        for object in qset:
            object.delete()
        
        return qset
        
      
def edit_offer(offer_id, price = None, course = None, condition = None, description = None):
    ''' Edit the offer with the new parameters if set
    '''
    qset = Offer.objects.filter(id=offer_id)
    for object in qset:
        if price != None:
            object.price = price
        if course != None:
            object.course = course 
        if condition != None:
            object.condition = condition
        if description != None:
            object.description = description
        object.save()  
        
def edit_auction(auction_id, course = None, condition = None, description = None):
    ''' Edit the auction with the new parameters if set
    '''
    qset = Auction.objects.filter(id=auction_id)
    for object in qset:
        if course != None:
            object.course = course 
        if condition != None:
            object.condition = condition
        if description != None:
            object.description = description
        object.save()  

def bid_auction(auction_id, current_price = None):
    ''' Update current_price of auction after bid
    '''
    qset = Auction.objects.filter(id=auction_id)
    for object in qset:
        if current_price != None:
            object.current_price = current_price
        object.save()