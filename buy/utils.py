from django.core.mail import send_mail, EmailMultiAlternatives
from TEX import settings
import sys

from_email =  settings.EMAIL_HOST_USER
subject = settings.EMAIL_SUBJECT_PREFIX

def notify_users(msg, addrs):
    ''' addrs is a list of email addresses'''
    #Send a simple 
    send_mail(subject, msg, from_email, addrs)
    
    #Send a formatted email with a backup in case HTML is no supported
    text_content = 'This is an important message.'
    html_content = '<p>This is an <strong>important</strong> message.</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, addrs)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
    
if __name__ == "__main__" :
    notify_users(sys.argv[1], [sys.argv[2]])
    
# Use
# export DJANGO_SETTINGS_MODULE=TEX.settings
# python utils.py "Testing Notification system" "jasala@princeton.edu"