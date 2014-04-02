from django.db import models

# Create your models here.
class Offer(models.Model):
    seller = models.CharField(max_length=100)
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
            books.append({'isbn':object.isbn, 'title':object.title, 'author':object.author, 'thumb':object.thumb})
    else:
        for object in qset:
            books.append({'isbn':object.isbn, 'title':object.title, 'author':object.author, 'cover':object.cover})

    return books
