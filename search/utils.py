from django.core.files import File
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
#     print get_book_info(title = query)
    return {"books":get_book_info(title = query)}
    
def search_by_author(query):
#     print get_book_info(author = query)
    return {"books":get_book_info(author = query)}

def search_by_course(query):
#     print get_course_list(course = query)
    return {"books":get_course_list(course = query)}

def search_by_isbn(query):
    result = get_book_info(isbn = query)
#     print result
    if result == []:
        info = fetch_isbn(query)
        update_book_cache(info["isbn"], info["title"], info["author"],
                info["frontcover"], info["thumbnail"])
        result = [info]
    
    return {"books":result}

###############################################


def fetch_isbn(isbn):
    URL = URL_STUB + isbn
    response = urllib2.urlopen(URL)
    result = json.load(response)
    
    # Check if search returned a match
    if result["totalItems"] == 0:
        print "No ISBN found"
        return
    
    elif result["totalItems"] > 1:
        print "ISBN is not unique"
        return
    
    info = {}
    book= result["items"][0]["volumeInfo"]
    
    info["isbn"] = isbn
    info["title"] = book["title"]
    info["author"] = "/".join(book["authors"])
    
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

if __name__ == '__main__':
    print search_by_isbn (sys.argv[1])