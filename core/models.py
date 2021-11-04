from django.db import models

# Create your models here.
from django.db.models.fields import CharField

class Products(models.Model):
    title=models.CharField(max_length=220)
    price=models.FloatField()
    discount=models.FloatField()
    description=models.TextField()
    
