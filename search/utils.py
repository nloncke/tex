from search.models import *
import sys
import urllib2
import json

URL_STUB="https://www.googleapis.com/books/v1/volumes?q=isbn:"
USER_AGENT=[("User-agent", "Mozilla/5.0")]
FNTCVR_STUB="media/frontcover_%s.jpg"
THUMB_STUB="media/thumbnail_%s.jpg"
FNTCVR_URL="/static/frontcover_%s.jpg"
THUMB_URL="/static/thumbnail_%s.jpg"


def search_by_title(query):
    return {"books":get_book_info(title = query)}
    
def search_by_author(query):
    return {"books":get_book_info(author = query)}

def search_by_course(query):
    return {"books":get_book_info(course = query)}

def search_by_isbn(query):
    result = get_book_info(isbn = query)
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
    
    info["author"] = "/".join(book["authors"])
    info["pub_date"] = book["publishedDate"]
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
###############################################


if __name__ == '__main__':
    print search_by_isbn (sys.argv[1])