from django.template.loader import render_to_string
from account.models import *
from buy.utils import email_users
from sys import argv


def get_book_info(isbn):
    from search.models import get_book_info
    return {"book":get_book_info(isbn = isbn, thumb=False)[0]}


# dummy for testing 
def get_followers(isbn):
    return ["aabdelaz", "lauraxu", "jasala", "nloncke"]


def notify_followers(isbn, offer):
    followers = get_followers(isbn)
    followers = map(lambda x: x + "@princeton.edu", followers)
    
    dict = get_book_info(isbn)
    dict['offer'] = offer
    
    html_msg = render_to_string("notify_newoffer.html", dict)
    text_msg = "A new offer is available for %s on tex" % dict["book"]["title"]
    
    frontcover =  dict["book"]["frontcover"]
    
    # For debugging
#     frontcover = "frontcover2.jpg"
    
    email_users(followers, html_msg, text_msg,frontcover, "New Offer Available")
    return
    
    
def put_offer(isbn, offer):
    from sell.models import put_offer
    new_offer_id = put_offer(isbn=isbn, offer=offer)
    notify_followers(isbn, offer)
    return new_offer_id
    
if __name__ == "__main__":
    notify_followers(argv[1], {})
    