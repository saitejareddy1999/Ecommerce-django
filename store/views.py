from django.shortcuts import render,get_object_or_404,redirect
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views  import _get_cart_id
from django.http import HttpResponse
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from .models import ReviewRating
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct
'''
intially we can see add to cart button in store page but we are not do like that instead of doing that just do view details if any user
is go to product detail page to add to cart button or else it is already added and we are required to view the button

'''
'''
for review 
if any user wants to review he want to login to system first and he want to purchase the particular product to review a product
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
    try:#1)
        single_product = Product.objects.get(category__slug = category_slug, slug = product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id =_get_cart_id(request),product = single_product).exists()#cart__ in cart model is the foreign key of cartItem,we have to filter based upon the single_product which is available if the element is already exists added into cart we return true 
     

    except Exception as e:#1)
        raise e
    if request.user.is_authenticated:
        try:#2)try block to check if the product is already purchased means he can submit the rating  so why we are checking in this view because we are in product_detail page  
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    context={
        'single_product' : single_product,
        'in_cart':in_cart,
        'orderproduct':orderproduct,
        'reviews':reviews,
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
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')#to get current page url
    if request.method == 'POST':#1)check request is post
        try:#if at all existing review is there by that particular user we can update it 
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)#if review is exist are notby taking current and product id user__id, we are writing __id because in review rating there is  user field in that user id is present we are taking foreign key for that to access id of while any user initialy adding product we can get particular id for that product
            form = ReviewForm(request.POST, instance=reviews)#in request.post  we are storing all the data wrto reviewrating form,why we are creating instance becuse if any user has that request we are just going on updating that if we dont pass that instance by default it will create new review 
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.') 
            return redirect(url)#after udating we are reuired to redirect to current page only so we want current page url so we can get by http_referer
        except ReviewRating.DoesNotExist:#to create a ne review
            form = ReviewForm(request.POST)#going to store a new record
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)
