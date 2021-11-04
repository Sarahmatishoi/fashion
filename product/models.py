from django.db import models
from django.db.models.fields import CharField


# Create your models here.
class Products(models.Model):
    name =models.CharField(max_length=15,null=True,blank=True)
    prices=models.IntegerField(null=True,blank=True)
    color=models.CharField(max_length=16,null=True,blank=True)
    size =models.CharField(max_length=10,null=True,blank=True)
    quantity=models.CharField(max_length=8,null=True,blank=True)
    product_image=models.ImageField(null=True,blank=True)
    
    
class Category(models.Model):
    category_name=models.CharField(max_length=16)
    category_description=models.TextField()


class Image(models.Model):
    image_name=models.CharField(max_length=16)
    image_id=models.CharField(max_length=8)

    
class Payments(models.Model):
    Account_name=models.CharField(max_length=8)
    phone_name=models.CharField(max_length=15)
    Amount=models.PositiveBigIntegerField()

class Order(models.Model):
    item_name=models.CharField(max_length=16)
    item_quantity=models.CharField(max_length=8)

class Sub_Category(models.Model):
    product_name=models.CharField(max_length=16)
    item_quantity=models.CharField(max_length=8)
