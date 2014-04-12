from django.db import models
from django.contrib.auth.models import User
from django_cas.backends import CASBackend

# Create your models here.
class BookUser(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    sell_list = models.CharField(max_length=500)
    watch_list = models.CharField(max_length=500)

    def __unicode__(self):
        return self.user.username




class PopulatedCASBackend(CASBackend):
    """CAS authentication backend with user data populated from AD"""

    def authenticate(self, ticket, service):
        """Authenticates CAS ticket and retrieves user data"""

        user = super(PopulatedCASBackend, self).authenticate(
            ticket, service)

        return user
