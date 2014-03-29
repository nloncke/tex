# from search import models
import sys
import urllib2
import json

URL_STUB="https://www.googleapis.com/books/v1/volumes?q=isbn:"
USER_AGENT=[("User-agent", "Mozilla/5.0")]
FNTCVR_STUB="../media/frontcover/%s.jpg"
THUMB_STUB="../media/thumbnail/%s.jpg"


# placeholders
def get_book_info(isbn = None, title = None, author = None, thumbnail = True): 
    return []
def get_course_list(course):
    pass
def update_book_cache(*toolazy):
    pass
#############################################

def search_by_title(query):
    return get_book_info(title = query)
    
def search_by_author(query):
    return get_book_info(author = query)

def search_by_course(query):
    return get_course_list(course = query)

def search_by_isbn(query):
    # query = convert_to_13(query)
    result = get_book_info(isbn = query)
    if result == []:
        result = fetch_isbn(query)
        update_book_cache(result["isbn"], result["title"], result["authors"],
                result["frontcover"], result["thumbnail"])
    
    return [result]


def convert_to_13(isbn):
    if len(isbn) == 13:
        return isbn
    if len(isbn) != 10:
        print "LAURA XUUUUU!!!!"
    
    

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
    info["authors"] = book["authors"]
#     authors = "/".join(book["authors"])

    
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
    except:
        frontcover = FNTCVR_STUB % "default"
        thumbnail = THUMB_STUB % "default"
    
    info["frontcover"] = frontcover
    info["thumbnail"] = thumbnail
    return info

if __name__ == '__main__':
    search_by_isbn (sys.argv[1])