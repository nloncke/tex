from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import HttpResponse
from TEX import settings
from search.models import *
import sys
MSG_STUB = "Yo! %s bought %s from %s for %s"

from_email =  settings.EMAIL_HOST_USER
subject = settings.EMAIL_SUBJECT_PREFIX

def email_users(msg, addrs):
    ''' addrs is a list of email addresses'''
    #Send a simple 
    send_mail(subject, msg, from_email, addrs)
    
    #Send a formatted email with a backup in case HTML is no supported
#     text_content = 'This is an important message.'
#     html_content = HttpResponse('<p>This is an <strong>important</strong> message.</p>')
#     msg = EmailMultiAlternatives(subject, text_content, from_email, addrs)
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()
#     print html_content
    

def notify_users(buyer, offer):
    buyer_email = "%s@princeton.edu" % buyer
    seller_email = "%s@princeton.edu" % offer["seller_id"]
    
    book = get_book_info(isbn=offer["isbn"], thumb = False)
    
    msg = MSG % buyer, book["title"], offer["seller_id"], offer["price"]   
    email_users(msg, [seller_email, buyer_email])
    
    return book
    

# Use
# export DJANGO_SETTINGS_MODULE=TEX.settings
# python utils.py "Testing Notification system" "jasala@princeton.edu"