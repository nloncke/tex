from django.template.loader import render_to_string
from book.models import get_followers
from buy.utils import email_users

def get_book_info(isbn):
    from search.models import get_book_info
    return {"book":get_book_info(isbn = isbn, thumb=False)[0]}

def get_title(isbn):
    result = get_book_info(isbn = isbn)[0]
    return result


def notify_followers(isbn, offer):
    followers = get_followers(isbn)
    followers = map(lambda x: x + "@princeton.edu", followers)
    
    dict = get_book_info(isbn)
    dict['offer'] = offer
    
    html_msg = render_to_string("notify_newoffer.html", dict)
    text_msg = "A new offer is available for %s on tex" % dict["book"]["title"]
    
    frontcover =  dict["book"]["frontcover"]
    
    # For debugging
    frontcover = "/app/buy/frontcover2.jpg"
    
    email_users(followers, html_msg, text_msg,frontcover, "New Offer Available")
    return
    
    
def put_offer(isbn, offer):
    from sell.models import put_offer
    new_offer_id = put_offer(isbn=isbn, offer=offer)
#     notify_followers(isbn, offer)
    return new_offer_id

    
if __name__ == "__main__":
    from sys import argv
    notify_followers(argv[1], {})
    