from django.db import models

# Create your models here.
class Test(models.Model):
    string = models.CharField(max_length=200)


def putTest(s):
    p = Test(string=s)
    p.save()

def getFirst():
    t = Test.objects.get(id=1)
    return t.string
