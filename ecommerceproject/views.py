from django.shortcuts import render
from store.models import Product,ReviewRating
def home(request):
    products = Product.objects.all().filter(is_available=True)#we are getting all the products from database & we are filtering from is_available if the product is available we are taking
    # and we are taking one context dictonary to store all the products in the dictoanary
    # Get the reviews
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
    context = {#we are required put it in render which should bo go to home page
        'products':products,
        'reviews':reviews
    }
    return render(request,'home.html',context)