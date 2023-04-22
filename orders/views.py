from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from carts.models import CartItem
from .forms import OrderForm
from.models import Order,Payment,OrderProduct
import datetime
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
#in placeorder page we need to show if there is an cart item we need to show makepayment button else we are not required to show it should go store page to select a product
# Create your views here.
def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])#by intializing this orderid we can get for user what are products he have ordered 

    # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],#all the transid payment method are there in order which i have take prder model from form 
        payment_method = body['payment_method'],
        amount_paid = order.order_total,#it is not inside the body we can get it from order model 
        status = body['status'],
    )
    payment.save()#this payment will record in the payment model

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)#because we want to take the variations of that particular id
        product_variation = cart_item.variations.all()#going to take all the variations to corresponding product
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)#we will get the orderproduct from model database because alreadyy we have saved that in above add this product_variation inside orderproduct
        orderproduct.variations.set(product_variation)#set all the variations inside orderprocduct
        orderproduct.save()

        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
    # Clear cart
    CartItem.objects.filter(user=request.user).delete()
    # Send order recieved email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
    
# Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)

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
            data.order_note = form.cleaned_data['order_note']#we required to get furtre feilds to store in order table we want tax & order_total we are defining it locally we are adding static values if we want dynamically need to create one model for tax->&tax
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
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)#user  is sending data from form after sending we are getting it by this query what the user is mentioned in form stroing it and sending it to payments page billing address
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
        # else:
        #     print(form.errors)
    else:
        return redirect('checkout')
def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html',context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
#     return render(request,'orders/order_complete.html')
# # def order_complete(request):
#     order_number = request.GET.get('order_number')
#     transID = request.GET.get('payment_id')

#     try:
#         order = Order.objects.get(order_number=order_number, is_ordered=True)
#         ordered_products = OrderProduct.objects.filter(order_id=order.id)

#         subtotal = 0
#         for i in ordered_products:
#             subtotal += i.product_price * i.quantity

#         payment = Payment.objects.get(payment_id=transID)

#         context = {
#             'order': order,
#             'ordered_products': ordered_products,
#             'order_number': order.order_number,
#             'transID': payment.payment_id,
#             'payment': payment,
#             'subtotal': subtotal,
#         }
#     return render(request, 'orders/order_complete.html')
#     except (Payment.DoesNotExist, Order.DoesNotExist):
#         return redirect('home')


            





    
