from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import HttpResponse
from TEX import settings
from search.models import *
import sys

from django.core.mail import EmailMessage
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


MSG_STUB = "Yo! %s bought %s from %s for %s"

from_email =  settings.EMAIL_HOST_USER
subject = settings.EMAIL_SUBJECT_PREFIX

def email_users(msg, addrs):
    ''' addrs is a list of email addresses'''
    #Send a simple 
#     send_mail(subject, msg, from_email, addrs)
    
#     Send a formatted email with a backup in case HTML is no supported
    text_content = 'This is an important message.'
    html_content = '<html><p>This is an <strong>important</strong> message.<img src="cid:image1"></p></html>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, addrs)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    

def notify_users(buyer, offer):
    buyer_email = "%s@princeton.edu" % buyer
    seller_email = "%s@princeton.edu" % offer["seller_id"]
    
    book = get_book_info(isbn=offer["isbn"], thumb = False)
    
    msg = MSG % buyer, book["title"], offer["seller_id"], offer["price"]   
    email_users(msg, [seller_email, buyer_email])
    
    return book
    
def email_2(addrs):
    # Load the image you want to send as bytes
    img_data = open('image.jpg', 'rb').read()
    
    # Create a "related" message container that will hold the HTML 
    # message and the image. These are "related" (not "alternative")
    # because they are different, unique parts of the HTML message,
    # not alternative (html vs. plain text) views of the same content.
    html_part = MIMEMultipart(_subtype='related')
    
    # Create the body with HTML. Note that the image, since it is inline, is 
    # referenced with the URL cid:myimage... you should take care to make
    # "myimage" unique
    body = MIMEText('<p>Hello <img src="cid:myimage" /></p>', _subtype='html')
    html_part.attach(body)
    
    # Now create the MIME container for the image
    img = MIMEImage(img_data, 'jpeg')
    img.add_header('Content-Id', '<myimage>')  # angle brackets are important
    img.add_header("Content-Disposition", "inline", filename="myimage") # David Hess recommended this edit
    html_part.attach(img)
    
    text_content = 'This is an important message.'
    
    # Configure and send an EmailMessage
    # Note we are passing None for the body (the 2nd parameter). You could pass plain text
    # to create an alternative part for this message
    msg = EmailMessage(subject, text_content, from_email, addrs)
    msg.attach(html_part) # Attach the raw MIMEBase descendant. This is a public method on EmailMessage
    msg.send()


if __name__ == "__main__":
    email_2([sys.argv[1]])
# Use
# export DJANGO_SETTINGS_MODULE=TEX.settings
# python utils.py "Testing Notification system" "jasala@princeton.edu"