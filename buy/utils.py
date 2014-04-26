from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from TEX import settings
from search.models import *
from django.template.loader import render_to_string

from_email =  settings.EMAIL_HOST_USER

TEXT_STUB = '%s has just purchased %s from %s for $%s. Please follow up with each other to seal the deal.'

def email_users(addrs, html_msg, text_msg, 
                frontcover="/static/frontcover_default.jpg",
                subject="", mass=False):
    
    subject = settings.EMAIL_SUBJECT_PREFIX + subject
    
    frontcover="media" + frontcover
    
    #REMOVE: For local dev
    addrs = [from_email if x == "tex@princeton.edu" else x for x in addrs]
    
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
        

def notify_users_bought(buyer, offer):
    buyer_email = "%s@princeton.edu" % buyer
    seller_email = "%s@princeton.edu" % offer["seller_id"]
    
    book = get_book_info(isbn=offer["isbn"], thumb = False)
    if book:
        book = book[0]
    else:
        return {}
     
    text_msg = TEXT_STUB % (buyer, book["title"], offer["seller_id"], offer["price"])
    offer["title"] = book["title"]
    html_msg = HTML_STUB % text_msg

    email_users([seller_email, buyer_email], html_msg, text_msg, book["frontcover"], 
                 "Transaction Complete")  
    return book



def notify_users_closed_auctions(auctions):
    '''
    Takes a list of inactive auctions
    
    TODO: notify the seller and highest bidder (if not "")
    That the auctions is closed and has been removed.
    
    '''
    
    pass



    

if __name__ == "__main__":
    import sys
    notify_users(sys.argv[1], {"seller_id":"jasala", "price": "700", "title":"The Practice of Programming",
                                 "isbn":"9780393979503"})