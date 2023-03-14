from django.shortcuts import render
from store.models import Product
def home(request):
    products = Product.objects.all().filter(is_available=True)#we are getting all the products from database & we are filtering from is_available if the product is available we are taking
    # and we are taking one context dictonary to store all the products in the dictoanary
    context = {#we are required put it in render which should bo go to home page
        'products':products,
    }
    return render(request,'home.html',context)