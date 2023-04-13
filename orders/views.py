from django.shortcuts import render,redirect
from django.http import HttpResponse
from carts.models import CartItem
from .forms import OrderForm
from.models import Order
import datetime
#in placeorder page we need to show if there is an cart item we need to show makepayment button else we are not required to show it should go store page to select a product
# Create your views here.

def place_order(request, total=0, quantity=0,):
    current_user = request.user

    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    print(cart_count)
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        print('inside if')
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            print('inside valid')
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            print(data.first_name,data.last_name)
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") 
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            return redirect('checkout')
    else:
        return redirect('checkout')
# def place_order(request,total = 0,quantity = 0):
#     current_user = request.user
#     # if the cart count is less than <=0 then redirect to store page
#     cart_items = CartItem.objects.filter(user = current_user)
#     cart_count = cart_items.count()
#     if cart_count <= 0:
#         return redirect('store')
#     # grand_total = 0
#     # tax = 0
#     # for cart_item in cart_items:
#     #     total += (cart_item.product.price * cart_item.quantity)
#     #     quantity = cart_item.quantity
#     # tax = (2 * total) / 100
#     # grand_total = total + tax
#     grand_total = 0
#     tax = 0
#     for cart_item in cart_items:
#         total += (cart_item.product.price * cart_item.quantity)
#         quantity += cart_item.quantity
#     tax = (2 * total)/100
#     grand_total = total + tax
    
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             #store all billing info at order table 
#             # we want to get instance of table
#             data = Order()
#             data.first_name = form.cleaned_data['first_name']
#             data.last_name = form.cleaned_data['last_name']
#             data.phone = form.cleaned_data['phone']
#             data.email = form.cleaned_data['email']
#             data.address_line_1 = form.cleaned_data['address_line_1']
#             data.address_line_2 = form.cleaned_data['address_line_2']
#             data.country = form.cleaned_data['country']
#             data.state = form.cleaned_data['state']
#             data.city = form.cleaned_data['city']
#             data.order_note = form.cleaned_data['order_note']#we required to get furtre feilds to store in order table we want tax & order_total we are defining it locally we are adding static values if we want dynamically need to create one model for tax->&tax
#             data.order_total = grand_total
#             data.tax = tax
#             data.ip = request.META.get('REMOTE_ADDR')
#             data.save()
#             # Generate order number
#             yr = int(datetime.date.today().strftime('%Y'))
#             dt = int(datetime.date.today().strftime('%d'))
#             mt = int(datetime.date.today().strftime('%m'))
#             d = datetime.date(yr,mt,dt)
#             current_date = d.strftime("%Y%m%d") 
#             order_number = current_date + str(data.id)
#             data.order_number = order_number
#             data.save()
#             return redirect('checkout')
#     else:
#         return redirect('checkout')
            





    
