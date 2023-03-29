from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views  import _get_cart_id
from django.http import HttpResponse
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
'''
intially we can see add to cart button in store page but we are not do like that instead of doing that just do view details if any user
is go to product detail page to add to cart button or else it is already added and we are required to view the button

'''

# Create your views here.
# def store(request,category_slug = None):
#     categories = None
#     products = None
#     if category_slug !=  None:#in databasee there is a slug
#         categories = get_object_or_404(Category,slug = category_slug )#if categories is found return that object otherwise it will return 404 
#         products = Product.objects.filter(category = categories,is_available =True)#this will bring us all our products from our category
#         product_count = products.count()

#     else:
#         products = Product.objects.all().filter(is_available=True)#we are getting all the products from database & we are filtering from is_available if the product is available we are taking
#         # and we are taking one context dictonary to store all the products in the dictoanary
#         product_count = products.count()
#     context = {#we are required put it in render which should bo go to home page
#         'products':products,
    
#         'product_count':product_count
#     }

#     return render(request,'store/store.html',context)
def store(request,category_slug = None):#for paginator
    categories = None
    products = None
    if category_slug !=  None:#in databasee there is a slug
        categories = get_object_or_404(Category,slug = category_slug )#if categories is found return that object otherwise it will return 404 
        products = Product.objects.filter(category = categories,is_available =True)#this will bring us all our products from our category
        paginator = Paginator(products,1)#there are 6 products initially we are getting here only 3 products
        page = request.GET.get('page')
        paged_products =paginator.get_page(page)#we are getting get request from here
        product_count = products.count()

    else:
        products = Product.objects.all().filter(is_available=True)#we are getting all the products from database & we are filtering from is_available if the product is available we are taking
        # and we are taking one context dictonary to store all the products in the dictoanary
        paginator = Paginator(products,3)#there are 6 products initially we are getting here only 3 products
        page = request.GET.get('page')
        paged_products =paginator.get_page(page)#we are getting get request from here
        product_count = products.count()
    context = {#we are required put it in render which should bo go to home page
        'products':paged_products,
    
        'product_count':product_count
    }

    return render(request,'store/store.html',context)



def product_detail(request,category_slug = None,product_slug = None):
    try:
        single_product = Product.objects.get(category__slug = category_slug, slug = product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id =_get_cart_id(request),product = single_product).exists()#cart__ in cart model is the foreign key of cartItem,we have to filter based upon the single_product which is available if the element is already exists added into cart we return true 
        
    except Exception as e:
        raise e
    context={
        'single_product' : single_product,
        'in_cart':in_cart,
    }
    return render(request,'store/product_detail.html',context)
def search(request):#here it is treating as category we are required to add infornt of any slug name which is getting w eare required to add category
    if 'keyword' in request.GET:#first we are checking if get request has this keyword or not
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains = keyword) | Q(product_name__icontains = keyword))
            product_count = products.count()
        context={
            'products':products,
            'product_count':product_count
        }
    return render(request,'store/store.html',context)