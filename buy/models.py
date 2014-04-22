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
    Returns the isbn, seller id, buyer_id and current_price of the given auction   
    If buy_now, return buy_now_price. 
    Also deletes it from database
    '''
    qset = Auction.objects.filter(id=auction_id)
    if len(qset) > 0:
        if buy_now == False:
            d =  { 'isbn': qset[0].isbn, 'seller_id':qset[0].seller_id, 'buyer_id':qset[0].buyer_id, 'price':qset[0].current_price }
        else:
            d =  { 'isbn': qset[0].isbn, 'seller_id':qset[0].seller_id, 'buyer_id':qset[0].buyer_id, 'price':qset[0].buy_now_price }
        qset[0].delete()
        return d
    else:
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

def bid_auction(auction_id, current_price, buyer_id):
    ''' Update current_price of auction after bid
        and update with new buyer
        
        TODO: Check if the current bid will be higher than 
        otherwise a race condition has occurred
        
        TODO: There should be error checking to ensure that 
        qset contains only one auction.
        
    '''
    qset = Auction.objects.filter(id=auction_id)
    for object in qset:
        if object.current_price < current_price:
            object.current_price = current_price    
            object.buyer_id = buyer_id
            object.save()
        return object.current_price
        
def get_current_price(auction_id):
    # get info of offer with given id
    # FILTER
    qset = Auction.objects.filter(id=auction_id)
    for object in qset:
        return object.current_price
    return None

def get_auction_isbn(auction_id):
    # get info of offer with given id
    # FILTER
    qset = Auction.objects.filter(id=auction_id)
    for object in qset:
        return object.isbn
    return None