from django.utils import timezone
from time import localtime, mktime 
from search.models import *
import sys

AMAZON_STUB = "http://www.amazon.com/gp/search/ref=sr_adv_b/?search-alias=stripbooks&field-isbn=%s"
CHEGG_STUB = "http://www.chegg.com/search/%s"
CAMPUS_STUB = "http://www.campusbooks.com/books/search.php?search_type=single&isbn=%s"
LABYRINTH_STUB = "http://www.labyrinthbooks.com/all_search.aspx?sisbn=%s"

def add_links(book_info):
    isbn = book_info["isbn"]
    book_info["amazon"] = AMAZON_STUB % isbn
    book_info["chegg"] = CHEGG_STUB % isbn
    book_info["campus"] = CAMPUS_STUB % isbn
    book_info["labyrinth"] = LABYRINTH_STUB % isbn
    return book_info
    

def get_book(isbn):
    ''' Return all the information necessary for the book page
        Returns an empty dictionary if the isbn is not in the database
        Fields are {book, amazon, chegg, ..., auctions, offers}
    '''
    book_info = get_book_info(isbn=isbn, thumb=False)
    if book_info == []:
        return {}
    
    # Get the first result
    if len(book_info) > 1:
        print "ERROR: ISBN should be unique"
        return None
    
    book_info = book_info[0]
    add_links(book_info)
    
    result = {"book":book_info}
    
    result["auctions"] = sorted(get_auctions(isbn), key=(lambda y:y["current_price"])) 
    result["offers"] = sorted(get_offers(isbn), key=(lambda x:x["buy_price"]))
    return result

if __name__ == "__main__" :
    print get_book(sys.argv[1])
    