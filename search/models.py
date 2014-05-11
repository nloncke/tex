from django.db import models
import os.path
import time
from TEX.settings import STATIC_ROOT

base = "."

# Create your models here.
class Offer(models.Model):
    seller_id = models.CharField(max_length=100)
    price = models.IntegerField()
    isbn = models.CharField(max_length=20)
    condition = models.CharField(max_length=100)
    description = models.CharField(max_length=800)
    course = models.CharField(max_length=200)
    def __unicode__(self):
        s = str(self.seller_id) + ' ' + str(self.price) + ' ' + self.isbn + ' ' + self.course + ' ' + self.condition
        return s

class Auction(models.Model):
    current_price = models.IntegerField()
    buy_now_price = models.IntegerField()
    buyer_id = models.CharField(max_length=100)
    seller_id = models.CharField(max_length=100)
    epoch = models.BigIntegerField()
    end_time = models.CharField(max_length=50)
    isbn = models.CharField(max_length=20)
    condition = models.CharField(max_length=100)
    description = models.CharField(max_length=800)
    course = models.CharField(max_length=200)
    def __unicode__(self):
        s = str(self.seller_id) + ' ' + str(self.current_price) + ' ' + self.isbn + ' ' + self.course + ' ' + self.condition
        return s


class Book(models.Model):
    isbn = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    frontcover = models.CharField(max_length=100)
    coverbytes = models.BinaryField()
    thumbnail = models.CharField(max_length=100)
    thumbbytes = models.BinaryField()
    pub_date = models.CharField(max_length=100) 
    course_list = models.CharField(max_length=300)
    amazon_price = models.CharField(max_length=20)
    price_stamp = models.IntegerField()
    def __unicode__(self):
        s = self.isbn + ' ' + self.title + ' ' + self.author + ' ' + self.frontcover + ' ' + self.thumbnail + ' ' + self.course_list
        return s

# 
def get_book_info(isbn = None, title = None, author = None, course = None, thumb = True):
    '''Return the book that matches exactly one of these fields.
       We assume that isbn will be an exact match, and that 
        title and author need not be
    '''
    books = []
    qset = Book.objects.all()

    if (isbn != None):
        qset = qset.filter(isbn=isbn)
    if (title != None):
        words = title.split()
        for word in words:
            qset = qset.filter(title__icontains=word)
    if (author != None):
        tokens = author.split()
        for token in tokens:
            qset = qset.filter(author__icontains=token)
    if (course != None):
        isbns = get_course_list(course)
        for object in isbns:
            newqset = qset.filter(isbn=object)
            for newob in newqset:
                if thumb == True:
                    thumbpath = base + newob.thumbnail
                    if not os.path.isfile(thumbpath):
                        with open(thumbpath, 'wb') as f:
                            f.write(newob.thumbbytes)
                    books.append({'isbn':newob.isbn, 'title':newob.title, 'author':newob.author, 'pub_date':newob.pub_date, 'thumbnail':newob.thumbnail, 'amazon_price':newob.amazon_price})
                else:
                    coverpath = base + newob.frontcover
                    if not os.path.isfile(coverpath):
                        with open(coverpath, 'wb') as f:
                            f.write(newob.coverbytes)
                    books.append({'isbn':newob.isbn, 'title':newob.title, 'author':newob.author, 'pub_date':newob.pub_date, 'frontcover':newob.frontcover, 'amazon_price':newob.amazon_price})

    elif (thumb == True):
        for object in qset:
            thumbpath = base + object.thumbnail
            if not os.path.isfile(thumbpath):
                with open(thumbpath, 'wb') as f:
                    f.write(object.thumbbytes)
        books = [{'isbn':object.isbn, 'title':object.title, 'author':object.author, 'thumbnail':object.thumbnail,'pub_date':object.pub_date, 'amazon_price':object.amazon_price} for object in qset]
    else:
        for object in qset:
            coverpath = base + object.frontcover  
            if not os.path.isfile(coverpath):
                with open(coverpath, 'wb') as f:
                    f.write(object.coverbytes)
        books = [{'isbn':object.isbn, 'title':object.title, 'author':object.author, 'frontcover':object.frontcover, 'pub_date':object.pub_date, 'amazon_price':object.amazon_price} for object in qset]

    sorted_books = sorted(books, key=lambda k: k['title']) 
    return sorted_books

# get isbns
def get_course_list(course):
    qset = Book.objects.filter(course_list__icontains=course)
    isbns = [object.isbn for object in qset]
    return set(isbns)

def update_book_cache(**book_info):
    with open(base + book_info['frontcover'], 'r') as f:
        book_info['coverbytes'] = f.read()
    with open(base + book_info['thumbnail'], 'r') as f:
        book_info['thumbbytes'] = f.read()
    book_info['course_list'] = ''
    book_info['price_stamp'] = 0
    book = Book(**book_info)
    book.save()

def get_auctions(isbn):
    '''
    Returns only active auctions
    Daemon will remove inactive auctions from the db, so 
    we don't have to do that here
    '''
    qset = Auction.objects.filter(isbn=isbn)
    qset = qset.filter(epoch__gt=time.time())
    auctions = [{'course':object.course, 'auction_id':object.id, 'current_price':object.current_price, 'buy_now_price':object.buy_now_price, 'buyer_id':object.buyer_id,
                 'seller_id':object.seller_id, 'end_time':object.end_time, 'condition':object.condition, 'description':object.description} for object in qset]
    return auctions

def get_offers(isbn):
    qset = Offer.objects.filter(isbn=isbn)
    offers = [{'course':object.course, 'offer_id':object.id, 'buy_price':object.price, 'seller_id':object.seller_id,
             'condition':object.condition, 'description':object.description} for object in qset]
    return offers

