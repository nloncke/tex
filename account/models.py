from django.db import models
from django.contrib.auth.models import User
from django_cas.backends import CASBackend
from search.models import *

# Create your models here.
class BookUser(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    watch_list = models.CharField(max_length=500)

    def __unicode__(self):
        return self.user.username

# returns list of offers of seller with the given id
def get_seller_offers(seller_id):
    return Offer.objects.filter(seller_id=seller_id)

def follow(user, isbn):
    bu = user.bookuser
    if bu.watch_list == '':
        bu.watch_list = isbn
    else:
        bu.watch_list = bu.watch_list + ' ' + isbn
    bu.save()

'''def get_follow_list(user):
    bu = user.bookuser
    return bu.watch_list'''

def unfollow(user, isbn):
    bu = user.bookuser
    tokens = bu.watch_list.split()
    if isbn in tokens:
        tokens.remove(isbn)
    bu.watch_list = ' '.join(tokens)
    bu.save()


def is_registered(user):
    ''' Returns True iff user already in already in our data base
    '''
    qset = User.objects.filter(username=user.username)
    if not qset:
        return False

    return True

def save_user(user, **info):
    ''' Save this user in our database with the information required
        The specification for info are TBD
    '''
    pass






# Maybe we don't need this
class PopulatedCASBackend(CASBackend):
    """CAS authentication backend with user data populated from AD"""

    def authenticate(self, ticket, service):
        """Authenticates CAS ticket and retrieves user data"""

        user = super(PopulatedCASBackend, self).authenticate(
            ticket, service)

        user.save()
        return user


