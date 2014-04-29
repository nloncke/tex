from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from TEX import settings
from search.models import *
from django.template.loader import render_to_string

from_email =  settings.EMAIL_HOST_USER

TEXT_STUB = '{0} has just purchased {1} from {2} for ${3}. Please follow up with each other to seal the deal.\
    \nBook Description: {4}\n{0} may not to purchase the book if it does not match this description.'
SAD_STUB = 'Hello %s,\nYour auction of %s has expired. You are welcome to auction it again or offer at a fixed price.'

def email_users(addrs, html_msg, text_msg, 
                frontcover="/static/frontcover_default.jpg",
                subject="", mass=False):
    
    subject = settings.EMAIL_SUBJECT_PREFIX + subject
    
    frontcover="media" + frontcover
    
    #REMOVE: For local dev
#     addrs = [from_email if x == "tex@princeton.edu" else x for x in addrs]
    
    # Create a "related" message container that will hold the HTML 
    # message and the image.
    html_part = MIMEMultipart(_subtype='related')
    
    # Create the body with HTML.
    body = MIMEText(html_msg, _subtype='html')
    html_part.attach(body)
    
    
    # Load the image you want to send as bytes
    try:
        with open(frontcover, 'rb') as f:
            img_data = f.read()
        # Now create the MIME container for the image
        img = MIMEImage(img_data, 'jpeg')
        img.add_header('Content-Id', '<frontcover>')
        img.add_header("Content-Disposition", "inline", filename="frontcover")
        html_part.attach(img)
    except :
        # Fail silently
        pass
        
    # Configure and send an EmailMessage
    if mass:
        msg = EmailMultiAlternatives(subject, None, from_email, bcc=addrs)
    else :
        msg = EmailMultiAlternatives(subject, None, from_email, addrs)
    msg.attach(html_part)
    msg.attach_alternative(text_msg, "text/plain")
    msg.send(True)
        

def notify_users_bought(buyer, offer, book={}):
    buyer_email = "%s@princeton.edu" % buyer
    seller_email = "%s@princeton.edu" % offer["seller_id"]
    
    book = get_book_info(isbn=offer["isbn"], thumb = False)
    if book:
        book = book[0]
    else:
        return {}
     
    text_msg = TEXT_STUB.format(buyer, book["title"], offer["seller_id"], 
                            offer["price"], offer["description"])
    offer["title"] = book["title"]
    offer["buyer_id"] = buyer
    html_msg = render_to_string("notify_bought.html", offer)
    
    email_users([seller_email, buyer_email], html_msg, text_msg, book["frontcover"], 
                 "Transaction Complete") 
    print text_msg 
    return book



def notify_users_closed_auctions():
    '''
    This function is called to clean up closed auctions
    Get all expired auctions
 
    for each auction:
        Check if there exists a highest bidder.
        
        If so, call notify_users_bought
        
        Otherwise, inform the seller of the bad news. 
        And that the auctions is closed and has been removed.
        
        See notify_users_bought and notify_nosale.html as guides
    '''
    from models import expired_auctions
    expired = expired_auctions()

    for object in expired:
        offer = {'course':object.course, 'offer_id':object.id, 'isbn':object.isbn,
                 'price':object.current_price, 
                 'seller_id':object.seller_id,'condition':object.condition}
        if object.buyer_id:
            notify_users_bought(object.buyer_id, offer)
        else:
            seller_email = "%s@princeton.edu" % object.seller_id
    
            book = get_book_info(isbn=object.isbn , thumb = False)
            if book:
                book = book[0]
            else:
                return {}
            
            book["seller_id"] = object.seller_id
     
            # Add the user name to reduce spam count
            text_msg = SAD_STUB % (object.seller_id, book["title"])
            html_msg = render_to_string("notify_nosale.html", book)
    
            email_users([seller_email], html_msg, text_msg, book["frontcover"], 
                 "Auction Expired")
    return


def notify_old_bidder(old_buyer, result):
    '''Notify the old bidder that they have been outbid '''
    
    to_addr = old_buyer + "@princeton.edu"
    
    html_msg = render_to_string("notify_outbid.html", result)
    text_msg = "You've been outbid in the auction for %s. \
    The new price is $%s.\n Auction ends on %s." % (result["title"], 
        result["current_price"], result["end_time"])
    
    email_users([to_addr], html_msg, text_msg, result["frontcover"], 
                "You've been outbid")
    
    

if __name__ == "__main__":
    import sys
    notify_users_bought(sys.argv[1], {"seller_id":"jasala", "price": "700",
         "end_time":"4/30/14 11:09", "current_price":"56", "isbn":"9780393979503",
         "description": "It's great!!"}
    , {"title":"The Practice of Programming", "frontcover":"/static/frontcover_9780393979503.jpg"}
                      )
