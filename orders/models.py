from django.db import models
from credentials.models import *
from product.models import *



class Address(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    contact_number = models.BigIntegerField()
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    pin_code = models.BigIntegerField()
    active = models.BooleanField(default=True)

class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    price = models.FloatField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

class ProductOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total = models.FloatField()