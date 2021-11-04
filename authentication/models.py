from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class User(models.Model):

    user_name=models.CharField(max_length=30)
    first_name=models.CharField(max_length=12)
    last_name=models.CharField(max_length=15)
    email=models.EmailField()
    password=models.CharField(max_length=10)
    confirm_password=models.CharField(max_length=10)
    