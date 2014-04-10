from django.db import models

# Create your models here.
class Offer(models.Model):
    seller = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    isbn = models.CharField(max_length=20)
    course = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    description = models.CharField(max_length=800)
    auction_id = models.IntegerField()
    def __str__(self):
        s = str(self.seller) + ' ' + str(self.price) + ' ' + self.isbn + ' ' + self.course + ' ' + self.condition
        return s


class Book(models.Model):
    isbn = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    cover = models.CharField(max_length=100)
    thumb = models.CharField(max_length=100)
    pub_date = models.CharField(max_length=100) 
    def __str__(self):
        s = self.isbn + ' ' + self.title + ' ' + self.author + ' ' + self.cover + ' ' + self.thumb
        return s

# we assume that isbn will be an exact match, and that 
# title and author need not be
def get_book_info(isbn = None, title = None, author = None, thumb = True):
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
    if (thumb == True):
        for object in qset:
            books.append({'isbn':object.isbn, 'title':object.title, 'author':object.author, 'thumbnail':object.thumb,'pub_date':object.pub_date})
    else:
        for object in qset:
            books.append({'isbn':object.isbn, 'title':object.title, 'author':object.author, 'frontcover':object.cover, 'pub_date':object.pub_date})

    return books

# get isbns
def get_course_list(course):
    isbns = []
    re = '.*' + course + '.*'
    qset = Offer.objects.filter(course__iregex=re)
    for object in qset:
        isbns.append(object.course)

def update_book_cache(isbn, title, author, frontcover, thumbnail, published_date):
    book = Book(isbn=isbn, title=title, author=author, cover=frontcover, pub_date=published_date, thumb=thumbnail)
    book.save()

# not dealing with auction stuff yet 
def get_offers(isbn):
    offers = []
    qset = Offer.objects.filter(isbn=isbn)
    for object in qset:
        offers.append({'offer_id':object.id, 'buy_price':object.price, 'seller_id':object.seller, 'condition':object.condition, 'description':object.description})

    return offers

