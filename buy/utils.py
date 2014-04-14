from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from TEX import settings
from search.models import *
from buy.messages import *
import sys

from_email =  settings.EMAIL_HOST_USER

def email_users(addrs, html_msg, text_msg, 
                frontcover="/static/frontcover_default.jpg",
                subject="", mass=False):
    
    subject = settings.EMAIL_SUBJECT_PREFIX + subject
    
    # Load the image you want to send as bytes
    img_data = open(frontcover, 'rb').read()
    
    # Create a "related" message container that will hold the HTML 
    # message and the image.
    html_part = MIMEMultipart(_subtype='related')
    
    # Create the body with HTML.
    body = MIMEText(html_msg, _subtype='html')
    html_part.attach(body)
    
    # Now create the MIME container for the image
    img = MIMEImage(img_data, 'jpeg')
    img.add_header('Content-Id', '<frontcover>')
    img.add_header("Content-Disposition", "inline", filename="frontcover")
    html_part.attach(img)
    
    # Configure and send an EmailMessage
    msg = EmailMultiAlternatives(subject, None, from_email, addrs)
    msg.attach(html_part)
    msg.attach_alternative(text_msg, "text/plain")
    msg.send()

def notify_users(buyer, offer):
    buyer_email = "%s@princeton.edu" % buyer
    seller_email = "%s@princeton.edu" % offer["seller_id"]
    
    book = get_book_info(isbn=offer["isbn"], thumb = False)
    if book:
        book = book[0]
    else:
        return {}
     
    text_msg = TEXT_STUB % (buyer, book["title"], offer["seller_id"], offer["price"])
    html_msg = HTML_STUB % text_msg

    # For debugging
    book["frontcover"] = "frontcover2.jpg"

    email_users([seller_email, buyer_email], html_msg, text_msg, book["frontcover"], 
                 "Transaction Complete")  
    return book
    

if __name__ == "__main__":
    notify_users(sys.argv[1], {"seller_id":"jasala", "price": "700", "title":"The Practice of Programming",
                                 "isbn":"9780393979503"})


# Use
# export DJANGO_SETTINGS_MODULE=TEX.settings
# python utils.py "Testing Notification system" "jasala@princeton.edu"


# 
# 
# def email_users(msg, addrs):
#     ''' addrs is a list of email addresses'''
    #Send a simple 
#     send_mail(subject, msg, from_email, addrs)
    
#     Send a formatted email with a backup in case HTML is no supported
#     text_content = 'This is an important message.'
#     html_content = '<html><p>This is an <strong>important</strong> message.<img src="cid:image1"></p></html>'
#     msg = EmailMultiAlternatives(subject, text_content, from_email, addrs)
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()
    