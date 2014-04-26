from django.template.loader import render_to_string
from book.models import get_followers
from buy.utils import email_users

def get_book_info(isbn):
    from search.models import get_book_info
    return {"book":get_book_info(isbn = isbn, thumb=False)[0]}

def notify_followers(offer, is_auction=False):
    isbn = offer["isbn"]
    followers = get_followers(isbn)
    followers = [x + "@princeton.edu" for x in followers]

    dict = get_book_info(isbn)
    dict["is_auction"] = is_auction
    
    dict['offer'] = offer
    html_msg = render_to_string("notify_newoffer.html", dict)
   
    if is_auction:
        subject = "An Auction has started"
        text_msg = "An auction has started for %s on tex" % dict["book"]["title"]
    else:
        subject = "New Offer Available"
        text_msg = "A new offer is available for %s on tex" % dict["book"]["title"]
    
    frontcover =  dict["book"]["frontcover"]
    
    email_users(followers, html_msg, text_msg, frontcover, subject, mass=True)
    return
    
    
def put_offer(offer):
    from sell.models import put_offer
    new_offer_id = put_offer(offer)
    notify_followers(offer)
    return new_offer_id


        
def validate_offer(offer):
    if offer["price"] == "0"|offer["condition"] == "0"|offer["description"] == "0"|offer["seller_id"] == "0":
        return False
    else:
        return True


def put_auction(auction):
    from sell.models import put_auction
    new_auction_id = put_auction(auction)
    notify_followers(auction, True)
    return new_auction_id

    
if __name__ == "__main__":
    from sys import argv
    notify_followers(argv[1], {})
    