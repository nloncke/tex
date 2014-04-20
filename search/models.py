from django.db import models
import os.path
from TEX.settings import BASE_DIR

# Create your models here.
class Offer(models.Model):
    seller_id = models.CharField(max_length=100)
    price = models.IntegerField()
    isbn = models.CharField(max_length=20)
    course = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    description = models.CharField(max_length=800)
    def __repr__(self):
        s = str(self.seller_id) + ' ' + str(self.price) + ' ' + self.isbn + ' ' + self.course + ' ' + self.condition
        return s

class Auction(models.Model):
    current_price = models.IntegerField()
    buy_now_price = models.IntegerField()
    buyer_id = models.CharField(max_length=100)
    seller_id = models.CharField(max_length=100)
    end_time = models.BigIntegerField()
    isbn = models.CharField(max_length=20)
    course = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    description = models.CharField(max_length=800)
    
class Book(models.Model):
    isbn = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    frontcover = models.CharField(max_length=100)
    coverbytes = models.BinaryField()
    thumbnail = models.CharField(max_length=100)
    thumbbytes = models.BinaryField()
    pub_date = models.CharField(max_length=100) 
    def __repr__(self):
        s = self.isbn + ' ' + self.title + ' ' + self.author + ' ' + self.frontcover + ' ' + self.thumbnail
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
        regex = '.*' + title + '.*' 
        qset = qset.filter(title__iregex=regex)
    if (author != None):
        tokens = author.split()
        for token in tokens:
            regex = '.*' + token + '.*'
            qset = qset.filter(author__iregex=regex)
    if (course != None):
        isbns = get_course_list(course)
        for object in isbns:
            newqset = qset.filter(isbn=object)
            for newob in newqset:
                if thumb == True:
				    thumbpath = '/app' + newob.thumbnail
                    if not os.path.isfile(thumbpath):
                        with open(thumbpath, 'wb') as f:
                            f.write(newob.thumbbytes)
                    books.append({'isbn':newob.isbn, 'title':newob.title, 'author':newob.author, 'pub_date':newob.pub_date, 'thumbnail':newob.thumbnail})
                else:
				    coverpath = '/app' + newob.frontcover
                    if not os.path.isfile(coverpath):
                        with open(coverpath, 'wb') as f:
                            f.write(newob.coverbytes)
                    books.append({'isbn':newob.isbn, 'title':newob.title, 'author':newob.author, 'pub_date':newob.pub_date, 'frontcover':newob.frontcover})

    elif (thumb == True):
        for object in qset:
            thumbpath = '/app' + object.thumbnail
            if not os.path.isfile(thumbpath):
                with open(thumbpath, 'wb') as f:
                    f.write(object.thumbbytes)
        books = [{'isbn':object.isbn, 'title':object.title, 'author':object.author, 'thumbnail':object.thumbnail,'pub_date':object.pub_date} for object in qset]
    else:
        for object in qset:
            coverpath = '/app' + object.frontcover  
            if not os.path.isfile(coverpath):
                with open(coverpath, 'wb') as f:
                    f.write(object.coverbytes)
        books = [{'isbn':object.isbn, 'title':object.title, 'author':object.author, 'frontcover':object.frontcover, 'pub_date':object.pub_date} for object in qset]

    return books

# get isbns
def get_course_list(course):
    re = '.*' + course + '.*'
    qset = Offer.objects.filter(course__iregex=re)
    isbns = [object.isbn for object in qset]
    return set(isbns)

def update_book_cache(**book_info):
    with open('/app' + book_info['frontcover'], 'r') as f:
        book_info['coverbytes'] = f.read()
    with open('/app' + book_info['thumbnail'], 'r') as f:
        book_info['thumbbytes'] = f.read()
    book = Book(**book_info)
    book.save()

# Dummy for auction stuff
def get_auctions(isbn):
    qset = Auction.objects.filter(isbn=isbn)
    auctions = [{'auction_id':object.id,'current_price':object.current_price, 'buy_now_price':object.buy_now_price, 'buyer_id':object.buyer_id,
                 'seller_id':object.seller_id, 'end_time':object.end_time, 'condition':object.condition, 'description':object.description} for object in qset]
    return auctions

def get_offers(isbn):
    qset = Offer.objects.filter(isbn=isbn)
    offers = [{'offer_id':object.id, 'buy_price':object.price, 'seller_id':object.seller_id,
             'condition':object.condition, 'description':object.description} for object in qset]
    return offers

