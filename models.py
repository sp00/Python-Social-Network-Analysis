from django.db import models
import datetime
from django.contrib.auth.models import User

class Threads(models.Model):
    num = models.CharField(max_length=10)
    title = models.CharField(max_length=200)

class Pairs(models.Model):
	CMC = models.CharField(max_length=10)
	sender = models.CharField(max_length=10)
	target = models.CharField(max_length=10) 

class Messages(models.Model):
    url = models.CharField(max_length=500)
    thread = models.CharField(max_length=20)
    tIndex = models.CharField(max_length=20)
    author = models.CharField(max_length=100)
    cmc = models.CharField(max_length=50)
    timestamp = models.DateTimeField('timestamp') 

    def __unicode__(self):
        return self.title

class Users(models.Model):
    uid = models.CharField(max_length=200)
    name = models.CharField(max_length=500)
    F_posts = models.CharField(max_length=3)
    J_posts = models.CharField(max_length=3)
    N_posts = models.CharField(max_length=3)

    def __unicode__(self):
        return self.uid

