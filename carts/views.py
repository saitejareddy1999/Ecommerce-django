from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product,Variation
from .models import Cart,CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
'''
1)we are creating cart.html to work template should work or not(this is mandatory to check if it is working or not)
2)a)it is for single prodcut in item we are going to add to cart whenever user is clicking add to cart button it should take me to cart page and it should add particular product to cart we dont have cart right that's when session comes into picture by using session we are required to add it to that we are required to create session function b)here we are going to store session keys as cart id's this is incrementing cart value dyanmically without authenticating
3)we are just directly going into cart view-->but here we are required to go with some content which is there like quantity,product how much for a product we are doing that operations in cart page 
4)we want to decrement the quantity before we have done increment the product now we are doing decrement and also we want to remove particular product also
5)in store page if any user clicks add to cart it should go into cart page(we are doing href in template page in cart.html)
6)if any user adding the product again into cart they are not required to add again to cart instead of that we are required to specify view cart(particular is already exists in cart for that we have go to single page  )
7)now we should make function for cart icon in context_processors using count function

'''
# Create your views here.
def _get_cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# first of all we require to add a button into cart write a function for that add to cart
# 1)def add_cart(request,product_id):#since we are adding product inside a cart we require product_id
#     
#         color = request.GET['color']
#         size = request.GET['size']
#     # return HttpResponse(color + '' + size)
#     # exit()
#     print(color,size)
#     product = Product.objects.get(id = product_id)#get the product  2)a
#     try:
#         cart = Cart.objects.get(cart_id=_get_cart_id(request))
#         # cart = Cart.objects.get(cart_id = _get_cart_id(request))#we need to get cart_id means seesion key which is stroing we need to bring that id from session get cart using cart_id present in session
#     except Cart.DoesNotExist:#if cart not exists
#         cart = Cart.objects.create(
#             cart_id = _get_cart_id(request)
#          )
#     cart.save()
#     #here we are required to create product and cart combine this product and cart we get the cartitem for increasing a item  2)b
#     try:
#         cart_item = CartItem.objects.get(product = product,cart = cart)#we are getting product from above product id
#         #we are getting cart from above cart because this going to create a cart_item
#         cart_item.quantity += 1#cartitem quantity to be incremented by one when we click on add cart it should be incremented
#         cart_item.save()
#     except CartItem.DoesNotExist:
#         cart_item = CartItem.objects.create(
#             product = product,
#             quantity = 1,
#             cart = cart
            
#         )
#         cart_item.save()
#     # return HttpResponse(cart_item.quantity)
#     # exit()
#     return redirect('cart')
# def remove_cart(request,product_id):#4)
#     cart = Cart.objects.get(cart_id = _get_cart_id(request))
#     product = get_object_or_404(Product,id = product_id)#if we have objects that is going to get or else it will get 404 not found
#     cart_item = CartItem.objects.get(product=product,cart=cart)
#     if cart_item.quantity > 1:
#         cart_item.quantity -= 1
#         cart_item.save()
#     else:
#         cart_item.delete()
#     return redirect('cart')
# def remove_cart_item(request,product_id):#4)
#     cart = Cart.objects.get(cart_id = _get_cart_id(request))
#     product = get_object_or_404(Product,id = product_id)
#     cart_item = CartItem.objects.get(product = product,cart = cart)
#     cart_item.delete()
#     return redirect('cart')
#2) def cart(request,total = 0,quantity = 0,cart_items =None):#cart_items for product information  3)
#     try:
#         tax = 0
#         grand_total = 0
#         cart = Cart.objects.get(cart_id = _get_cart_id(request))
#         cart_items = CartItem.objects.filter(cart = cart , is_active = True)#brings all cart items
#         for cart_item in cart_items:
#             total += cart_item.product.price * cart_item.quantity
#             quantity = cart_item.quantity
#         tax = (2 * total) / 100
#         grand_total = total + tax
#     except ObjectDoesNotExist:
#         pass# just ignore
#     context = {
#         'total': total, #all cart prices
#         'quantity' : quantity,
#         'cart_items':cart_items,
#         'tax'       : tax,
#         'grand_total':grand_total
#     }
#     return render(request,'store/cart.html',context)
# ------------------------------
# variation purpose we are making it with post request
def add_cart(request,product_id):#since we are adding product inside a cart we require product_id
    product = Product.objects.get(id = product_id)#we will get proper variation for a specific product
    #we will add many products so we are required add alll variations for specific product
    product_variation = []
    if request.method == 'POST':

        # color = request.POST['color'] upto here we are doing for only for color and size if any variation comes there is a problem so we have to handle that situation for that we are looping over post request and we are getting
        # size = request.POST['size']
        for item in request.POST:
            key = item
            value = request.POST[key]#we are getting specified value ex:if we have color it wil store in key after we are get post request from respective key 
            #we have to check if the corresponding values are comming from speified product or not
            try:
                variation = Variation.objects.get(product = product,variation_category__iexact = key, variation_value__iexact = value)
                product_variation.append(variation)#we can store this values inside a cart item for every particular product we need to add specified color and size variations what we have given
            except:
                pass
    # return HttpResponse(color + '' + size)
    # exit()
    
      
    try:
        cart = Cart.objects.get(cart_id=_get_cart_id(request))
        # cart = Cart.objects.get(cart_id = _get_cart_id(request))#we need to get cart_id means seesion key which is stroing we need to bring that id from session get cart using cart_id present in session
    except Cart.DoesNotExist:#if cart not exists
        cart = Cart.objects.create(
            cart_id = _get_cart_id(request)
         )
    cart.save()
    #here we are required to create product and cart combine this product and cart we get the cartitem for increasing a item  2)b

    #grouping variation
    # we need to think if the cart item is coming with same product and same variations we need to group that item so we need to chek if cart item is exists in cart or not  if it exists we need to increase that particular cartitem  or elsse need add that in cart
    is_cart_item_exists = CartItem.objects.filter(product = product,cart = cart).exists()#it will return true or false
    if is_cart_item_exists:
        # cart_item = CartItem.objects.get(product = product,cart = cart)#we are getting product from above product id
        # cart_item = CartItem.objects.create(product = product,quantity = 1,cart = cart)#whenever same product comes with  different variation 
        cart_item = CartItem.objects.filter(product = product,cart = cart)#we are just filterig based in product and cart to get cart_item is present in cart or not
        #we need three points to check if is there or not
            #existing variations need to check if that product with similar variations are there o not need to iterate
            #current products#product_variation
            #item_id
        ex_var_list = []   
        id = [] 
        for item in cart_item:
            existing_variation = item.variations.all() #we are all the items which are there in cart so we have so many items cart we need to add it in list
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
        print(ex_var_list)
        
        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)#2)we are getting id from product variation 
            item_id = id[index]
            item = CartItem.objects.get(product = product,id = item_id )#1)we want to get item id for which variation is coming so we need can get from that
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(product = product,quantity = 1,cart = cart)#whenever same product comes with  different variation
            if len(product_variation) > 0:#variation multiple items for different products all are combined
                item.variations.clear()
                item.variations.add(*product_variation)
            # cart_item.quantity += 1#cartitem quantity to be incremented by one when we click on add cart it should be incremented
            item.save()
    else:#new cart item also we are adding 
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
            
        )
        if len(product_variation) > 0:#variation multiple iteems for different products all are combined
            cart_item.variations.clear()#to clear what are added upto now
            cart_item.variations.add(*product_variation)#*for adding 
        cart_item.save()
    # return HttpResponse(cart_item.quantity)
    # exit()
    return redirect('cart')
def remove_cart(request,product_id,cart_item_id):#4)while doing variations we require to add cart_item.id to delete the product
    cart = Cart.objects.get(cart_id = _get_cart_id(request))
    product = get_object_or_404(Product,id = product_id)#if we have objects that is going to get or else it will get 404 not found
    try:
        cart_item = CartItem.objects.get(product=product,cart=cart,id = cart_item_id )
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')
def remove_cart_item(request,product_id,cart_item_id):#4)
    cart = Cart.objects.get(cart_id = _get_cart_id(request))
    product = get_object_or_404(Product,id = product_id)
    cart_item = CartItem.objects.get(product = product,cart = cart,id = cart_item_id)
    cart_item.delete()
    return redirect('cart')
def cart(request,total = 0,quantity = 0,cart_items =None):#cart_items for product information  3)
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id = _get_cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart , is_active = True)#brings all cart items
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity = cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass# just ignore
    context = {
        'total': total, #all cart prices
        'quantity' : quantity,
        'cart_items':cart_items,
        'tax'       : tax,
        'grand_total':grand_total
    }
    return render(request,'store/cart.html',context)
# -----------------
# if len(product_variation) > 0:#variation multiple iteems for different products all are combined
#                 cart_item.variations.clear()
#                 for item in product_variation:
#                     cart_item.variations.add(item)