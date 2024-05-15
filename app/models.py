from django.db import models

from django.contrib.auth.models import User


class Product(models.Model):
    name=models.CharField(max_length=100) 
    image=models.ImageField(upload_to='products/') 
    price=models.PositiveIntegerField(default=0) 
    quantity=models.PositiveIntegerField(default=0) 
    dprice=models.PositiveIntegerField(default=0) 

    CATEGORY_CHOICES = [
    ('fruits', 'Fruits'),
    ('vegetables', 'Vegetables'),
        # Add more categories as needed
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES,default='fruits')

    def __str__(self):
        return self.name


class Cart(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    
    def __str__(self):
        return f"{self.product} {self.quantity}"



class Billing(models.Model):
    userName = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin = models.CharField(max_length=100)
    payment_method=models.CharField(max_length=100)
    amount=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.userName} {self.payment_method}"
    
class FarmerRequest(models.Model):
    name =models.CharField(max_length=200)    
    email =models.CharField(max_length=200)    
    address =models.CharField(max_length=200)    
    reqmsg =models.TextField(max_length=200)  

    def __str__(self):
        return self.name  
     
