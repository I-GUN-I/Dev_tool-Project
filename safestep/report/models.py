from django.db import models
from django.contrib.auth.models import *


class Contact(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=500)

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete= models.PROTECT)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=500)
    contact = models.ForeignKey(Contact,on_delete = models.CASCADE, null=True)

class Sensor(models.Model):
    speed =  models.IntegerField()
    location = models.CharField(max_length=500)
    

class FallEvent(models.Model):
    user = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    sensor = models.ForeignKey(Sensor,on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.user_id} - {self.timestamp}"

class TwilioAPI(models.Model):
    account_sid = models.CharField(max_length=40)
    auth_token = models.CharField(max_length=40)
    tel = models.CharField(max_length=20)
