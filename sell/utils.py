from search import models
import sell


def get_book_info(isbn):
    return {"book":models.get_book_info(isbn = isbn, thumb=False)[0]}


def put_offer(isbn, offer):
    return sell.models.put_offer(isbn=isbn, offer=offer, course=offer["course"])