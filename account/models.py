from django.db import models
from django.contrib.auth.models import User
from django_cas.backends import CASBackend
from search.models import *

# Create your models here.
class BookUser(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    sell_list = models.CharField(max_length=500)
    watch_list = models.CharField(max_length=500)

    def __unicode__(self):
        return self.user.username

# returns list of offers of seller with the given id
def get_seller_offers(seller_id):
    return Offer.objects.filter(seller_id=seller_id)

class PopulatedCASBackend(CASBackend):
    """CAS authentication backend with user data populated from AD"""

    def authenticate(self, ticket, service):
        """Authenticates CAS ticket and retrieves user data"""

        user = super(PopulatedCASBackend, self).authenticate(
            ticket, service)

        return user
