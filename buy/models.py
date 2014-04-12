from django.db import models
from search.models import *
from account.models import *

# returns the isbn and seller id of the given offer
def get_offer(offer_id):
    qset = Offer.objects.filter(id=offer_id)
    if len(qset) > 0:
        return { 'isbn': qset[0].isbn, 'seller_id':qset[0].seller }

    else:
        return None
