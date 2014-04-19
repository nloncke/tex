from django.db import models
from account.models import *

# Create your models here.

def get_followers(isbn):
    ''' Return a list of user_id of all user that are following
    this book 
    '''
    regex = '.*' + isbn + '.*'
    qset = BookUser.objects.filter(watch_list__iregex=regex)

    followers = []
    for object in qset:
       	followers.append(object.user.username)
		
    return followers
