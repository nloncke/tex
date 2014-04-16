from search.models import *
import sys

AMAZON_STUB = "http://www.amazon.com/gp/search/ref=sr_adv_b/?search-alias=stripbooks&field-isbn=%s"
CHEGG_STUB = "http://www.chegg.com/search/%s"
CAMPUS_STUB = "http://www.campusbooks.com/books/search.php?search_type=single&isbn=%s"
LABYRINTH_STUB = "http://www.labyrinthbooks.com/all_search.aspx?sisbn=%s"


def get_book(isbn):
    book_info = get_book_info(isbn=isbn, thumb=False)
    if book_info == []:
        return None
    # Get the first result
    if len(book_info) > 1:
        print "ERROR: ISBN should be unique"
        return None
    
    book_info = book_info[0]
    book_info["amazon"] = AMAZON_STUB % isbn
    book_info["chegg"] = CHEGG_STUB % isbn
    book_info["campus"] = CAMPUS_STUB % isbn
    book_info["labyrinth"] = LABYRINTH_STUB % isbn
    
    result = {"book":book_info}
    result["offers"] = sorted(get_offers(isbn), key=(lambda x:x["buy_price"]))
    return result


if __name__ == "__main__" :
    print get_book(sys.argv[1])
    