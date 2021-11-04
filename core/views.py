from django.shortcuts import render

# Create your views here.

from .models import Products
from django.core .paginator import Page, Paginator




def base(request):
    product_objects = Products.objects.all()

     #search
    item_name = request.GET.get("item_name")
    if item_name !='' and item_name is not None:
        product_objects=product_objects.filter(title__icontains=item_name)

        #paginator    
    paginator=Paginator(product_objects, 4)
    page= request.GET.get('page')
    product_objects=paginator.get_page(page)

    return render(request, 'shop/index.html',{'product_objects': product_objects})
    #Getting the details for each product using id
def detail(request, id):
    product_object= Products.objects.get(id=id)
    return render(request, 'shop/detail.html',{'product_object': product_object})
