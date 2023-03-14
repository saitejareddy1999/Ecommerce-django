from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import Category

# Create your views here.
def store(request,category_slug = None):
    categories = None
    products = None
    if category_slug !=  None:#in databasee there is a slug
        categories = get_object_or_404(Category,slug = category_slug )#if categories is found return that object otherwise it will return 404 
        products = Product.objects.filter(category = categories,is_available =True)#this will bring us all our products from our category
        product_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True)#we are getting all the products from database & we are filtering from is_available if the product is available we are taking
        # and we are taking one context dictonary to store all the products in the dictoanary
        product_count = products.count()
    context = {#we are required put it in render which should bo go to home page
        'products':products,
        'product_count':product_count
    }

    return render(request,'store/store.html',context)


def product_detail(request,category_slug = None,product_slug = None):
    single_product = Product.objects.get(category__slug = category_slug, slug = product_slug)
    context={
        'single_product' : single_product,
    }
    return render(request,'store/product_detail.html',context)