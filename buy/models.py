from search.models import *
from account.models import *

# returns the isbn and seller id of the given offer
def get_offer(offer_id):
    qset = Offer.objects.filter(id=offer_id)
    if len(qset) > 0:
        # remove offer from seller field 
        seller = BookUser.objects.filter(id=qset[0].seller_id)                                                                                                    
        if len(seller) > 0:
            tokens = seller[0].sell_list.split()
            tokens.remove(qset[0].isbn)
            ' '.join(tokens)

        return { 'isbn': qset[0].isbn, 'seller_id':qset[0].seller }


    else:
        return None

