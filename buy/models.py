from search.models import *
from account.models import *

# returns the isbn and seller id of the given offer
# also deletes it from database
def get_offer(offer_id):
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
        return None

def edit_offer(offer_id, price = None, course = None, condition = None, description = None, auction_id = None):
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
        if auction_id != None:
            object.auction_id = auction_id

        object.save()
