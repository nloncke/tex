from search import models


def get_book_info(isbn):
    return {"book":models.get_book_info(isbn = isbn, thumb=False)[0]}