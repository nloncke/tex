from search.models import *
from account.models import *

def remove_offer(offer_id):
    '''
    Returns the isbn, seller id and price of the given offer
    Also deletes it from database
    '''
    qset = Offer.objects.filter(id=offer_id)
    if len(qset) > 0:
        # remove offer from seller field 
        seller = BookUser.objects.filter(id=qset[0].seller_id)                                                                                                    
        if len(seller) > 0:
            tokens = seller[0].sell_list.split()
            tokens.remove(qset[0].isbn)
            ' '.join(tokens)
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

def get_offer_info(offer_id):
    qset = Offer.objects.filter(id=offer_id)
    for object in qset:
