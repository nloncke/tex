from django.db import models
from django.contrib.auth.models import User
from django_cas.backends import CASBackend
from search.models import *

# Create your models here.
class BookUser(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    watch_list = models.CharField(max_length=500)
    default_search = models.CharField(max_length=30)
    class_year = models.CharField(max_length=5)
    
    def __unicode__(self):
        return self.user.username
        

# returns list of offers of seller with the given id
def get_seller_offers(seller_id):
    return Offer.objects.filter(seller_id=seller_id)

def get_seller_auctions(seller_id):
    qset = Auction.objects.filter(epoch__gt=time.time()) 
    return qset.filter(seller_id=seller_id)

def follow(user, isbn):        
    bu = user.bookuser
    if bu.watch_list == '':
        bu.watch_list = isbn
    else:
        bu.watch_list = bu.watch_list + ' ' + isbn
    bu.save()


def get_follow_list(user):
  
    bu = user.bookuser
    return bu.watch_list.split(' ')

def unfollow(user, isbn):
    bu = user.bookuser
    tokens = bu.watch_list.split()
    if isbn in tokens:
        tokens.remove(isbn)
    bu.watch_list = ' '.join(tokens)
    bu.save()


def not_registered(user):
    ''' Returns False iff user already in already in our data base
    '''
    try:
        qset = BookUser.objects.get(user__username=user.username)
        return False
    except BookUser.DoesNotExist:
        return True
    
    # Throw exception if multiple objects returned


def save_user(user, **info):
    ''' Save this user in our database with the information required
        The specification for info are TBD
        
        info is a dictionary with "class_year" and "default_search"
    '''
    user.bookuser.class_year = info['class_year']
    user.bookuser.default_search = info['default_search']
    user.bookuser.save()



class PopulatedCASBackend(CASBackend):
    """CAS authentication backend with user data populated from AD"""

    def authenticate(self, ticket, service):
        """Authenticates CAS ticket and retrieves user data"""
        
        user = super(PopulatedCASBackend, self).authenticate(
            ticket, service)
            
        if not_registered(user):
            bu = BookUser(user=user, watch_list='', default_search='title', class_year='')
            bu.save()  

        return user


