from search.models import *
import sys
import urllib2
import json
import re
from TEX.settings import BASE_DIR

URL_STUB="https://www.googleapis.com/books/v1/volumes?q=isbn:"
USER_AGENT=[("User-agent", "Mozilla/5.0")]
FNTCVR_STUB= 'media/static/frontcover_%s.jpg'
THUMB_STUB= 'media/static/thumbnail_%s.jpg'
FNTCVR_URL="/static/frontcover_%s.jpg"
THUMB_URL="/static/thumbnail_%s.jpg"


def search_by_title(query):
    return {"books":get_book_info(title = query)}
    
def search_by_author(query):
    return {"books":get_book_info(author = query)}

def search_by_course(query):
    return {"books":get_book_info(course = query)}

def search_by_isbn(query, thumb=True):
    result = get_book_info(isbn = query, thumb=thumb)
    if result == []:
        info = fetch_isbn(query)
        if info:
            update_book_cache(**info)
            result = [info]
    
    return {"books":result}
###############################################


def fetch_isbn(isbn):
    ''' Scrape googleapis for the data about the book
    Return the first match if it exists.
    Some times, google books returns more than one item 
    See https://www.googleapis.com/books/v1/volumes?q=isbn:9780393979503
    '''
    URL = URL_STUB + isbn
    response = urllib2.urlopen(URL)
    result = json.load(response)
    
    # Check if search returned a match
    if result["totalItems"] == 0:
        return []
    
    info = {}
    book= result["items"][0]["volumeInfo"]
    
    info["isbn"] = isbn
    try:
        info["title"] = ": ".join((book["title"], book["subtitle"]))
    except:
        info["title"] = book["title"]
    
    try:
        info["author"] = "/".join(book["authors"])
    except: 
        info["author"] = "This book as no registered authors :o"
    
    try:
        info["pub_date"] = book["publishedDate"]
    except:
        info["pub_date"] = "No published date available"
    try:
        url_fnt = book["imageLinks"]["thumbnail"].split("&edge")[0]
        url_thm = book["imageLinks"]["smallThumbnail"].split("&edge")[0]
        opener = urllib2.build_opener()
        opener.addheaders = USER_AGENT
        img = opener.open(url_fnt)
        frontcover = FNTCVR_STUB % isbn
        with open(frontcover, "wb") as f:
            f.write(img.read())
        img = opener.open(url_thm)
        thumbnail = THUMB_STUB % isbn
        with open(thumbnail, "wb") as f:
            f.write(img.read())
        # Set to the right url
        frontcover = FNTCVR_URL % isbn
        thumbnail = THUMB_URL % isbn    
    except:
        frontcover = FNTCVR_URL % "default"
        thumbnail = THUMB_URL % "default"
    
    info["frontcover"] = frontcover
    info["thumbnail"] = thumbnail
    return info

def validate_isbn(isbn):
    regex = re.compile("(^((\s)*([0-9]-?){9}[0-9Xx](\s)*)$)|(^((\s)*(97[89]-?([0-9]-?){9}[0-9])(\s)*)$)")
    if regex.search(isbn):
        # Remove non ISBN digits, then split into an array
        chars = list(str(re.sub("[^0-9Xx]", "", isbn)))
        # Remove the final ISBN digit from `chars`, and assign it to `last`
        last  = chars.pop()  
        if len(chars) == 9:
        # Compute the ISBN-10 check digit
            val = sum((x + 2) * int(y) for x,y in enumerate(reversed(chars)))
            check = 11 - (val % 11)
            if check == 10:
                check = "X"
            elif check == 11:
                check = "0"
        else:
        # Compute the ISBN-13 check digit
            val = sum((x % 2 * 2 + 1) * int(y) for x,y in enumerate(chars))
            check = 10 - (val % 10)
            if check == 10:
                check = "0"    
        if (str(check) == last):
            #print "Valid ISBN"
            return True
        else:
            #print "Invalid ISBN check digit"
            return False
    else:
        #print "Invalid ISBN"
        return False

def validate_title(title):
    regex = re.compile("^[\w\s]{1,200}$")
    if re.search(regex, title):
        return True
    else:
        return False
        
def validate_author(author):
    regex = re.compile("^[a-zA-Z\s]{1,100}$")
    if re.search(regex, author):
        return True
    else:
        return False

def validate_course(course):
    regex = re.compile("(\s)*[a-zA-Z]{3}( )*[0-9]{3}(\s)*$")
    if re.search(regex, course):
        return True
    else:
        return False
        
def convert_to_13(isbn):
    if len(isbn) == 13:
        return isbn
    if len(isbn) == 10:
        chars = '978'
        chars = list(chars + isbn)
        chars.pop()
        val = sum((x % 2 * 2 + 1) * int(y) for x,y in enumerate(chars))
        check = 10 - (val % 10)
        if check == 10:
            check = "0"
        chars.append(str(check))
        return ''.join(chars)
    else:
        return 0
###############################################


if __name__ == '__main__':
    print search_by_isbn (sys.argv[1])