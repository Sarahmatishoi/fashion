from django.contrib import admin
from .models import Category,Order, Payments, Products, Sub_Category

# Register your models here.


# Register your models here.
admin.site.register(Products)
admin.site.register(Category)
admin.site.register(Payments)
admin.site.register(Order)
admin.site.register(Sub_Category)