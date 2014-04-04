from django.db import models

# Create your models here.
class Offer(models.Model):
    seller = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    isbn = models.CharField(max_length=20)
    course = models.CharField(max_length=100)

class Book(models.Model):
    isbn = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    cover = models.CharField(max_length=100)
    thumb = models.CharField(max_length=100)

# we assume that isbn will be an exact match, and that 
# title and author need not be
def get_book_info(qisbn = None, qtitle = None, qauthor = None, thumb = True):
    books = []
    qset = Book.objects.all()

    if (qisbn != None):
        qset = qset.filter(isbn=qisbn)
    if (qtitle != None):
        regex = '.*' + qtitle + '.*' 
        qset = qset.filter(title__regex=regex)
    if (qauthor != None):
        regex = '.*' + qauthor + '.*'
        qset = qst.filter(author__regex=regex)
    
    if (thumb == True):
        for object in qset:
            books.append({'isbn':object.isbn, 'title':object.title, 'author':object.author, 'thumbnail':object.thumb})
    else:
        for object in qset:
            books.append({'isbn':object.isbn, 'title':object.title, 'author':object.author, 'frontcover':object.cover})

    return books

# get isbns
def get_course_list(course):
    isbns = []
    re = '.*' + course + '.*'
    qset = Offer.objects.filter(course__regex=re)
    for object in qset:
        isbns.append(object.course)

def update_book_cache(isbn, title, author, cover, thumb):
    book = Book(isbn=isbn, title=title, author=author, cover=cover, thumb=thumb)
    book.save()

# not dealing with auction stuff yet 
def get_offers(isbn):
    offers = []
    qset = Offer.objects.filter(isbn=isbn)
    for object in qset:
        offers.append({'offer_id':object.id, 'buy_price':object.price, 'seller_id':object.seller})

    return offers

