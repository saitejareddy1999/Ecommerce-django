from django.shortcuts import render,redirect
from .forms import RegistrationForm
from accounts.models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from carts.models import Cart,CartItem
from carts.views import _get_cart_id
import requests

#Activation email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)#request.post will contain ALL THE field values
        if form.is_valid():
            first_name   = form.cleaned_data['first_name']
            
            #when u use forms we require to fetch the data from request which user is provided
            last_name    = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email        = form.cleaned_data['email']
            password     = form.cleaned_data['password']
            print('first_name','last_name','phone_number','password')
            username     = email.split('@')[0]
            user         = Account.objects.create_user(first_name = first_name,last_name = last_name, email = email,password = password,username = username )#if u verify with create user we have created in accounts functionality if u add thos e feilds it will shw is_active button turned on
            user.phone_number = phone_number
            user.save()
            #USER ACTIVATION
            current_site = get_current_site(request)#getting localhost site
            mail_subject = 'please activate your account'
            message = render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),#are doing primary key encoding with this work so,no body can see this userid
                'token':default_token_generator.make_token(user),#we are declaring for this user and making a token for that partiular user
            })
            to_email = email#we are getting mail for user which is specifying
            send_email = EmailMessage(mail_subject,message,to = [to_email])#we are sending with these details
            send_email.send()
            # messages.success(request,'Registration done succesfully')
            return redirect('/accounts/login/?command=verification&email='+email)



    else:#registration form should render
        form = RegistrationForm()
    context = {
        'form':form
        }
    
    return render(request,'accounts/register.html',context)
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user =auth.authenticate(email = email,password = password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id = _get_cart_id(request))#we are getting the cart id which we are pushing insidethe user
                is_cart_item_exists = CartItem.objects.filter(cart = cart).exists()#product = product,#here we are not adding products because just we are making what are items inside cart just assigining it to user
                if is_cart_item_exists:#we  are going to get all the cartitem inside what are there and we are assigning it to user
                    cart_item = CartItem.objects.filter(cart = cart)# here we need to check if the user is not logged andd added products to cart,but after the user comes logged in there is same type of product in cart we are grouping that product and increaing the quantity
                    #getting product variations from cartitem and getting what user wants variation we are grouping them
                    product_variation = []#getting the product_variations by cart_id
                    for item in cart_item:
                        variation = item.variations.all() #we are getting variations from added into cartd
                        product_variation.append(list(variation))

                    #what user is adding the need to grp that vsriations only
                    cart_item = CartItem.objects.filter(user = user)#we are just filterig based in product and cart to get cart_item is present in cart or not
                    ex_var_list = []  #get the cartitems from user to  access his product variations
                    id = [] 
                    for item in cart_item:
                        existing_variation = item.variations.all() #we are all the items which are there in cart so we have so many items cart we need to add it in list
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    # PRODUCT_Variation = [1,2,3,4,6]
                    # ex_variation=[4,6,7,8]#we need to group those common elements from both lists
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id = item_id)
                            item.quantity += 1
                            item.user = user #those products assign to who are loggedin user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart = cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request,user)
            messages.success(request,'you are logged in')
            #instead of going to dashboard we aare dynamically moving next page measn checkout which is getting in url path and we split that into two parts key and value if the lkey is present we are redireting to cart page but to handle this there are various approaches to do but here we are doing reuests module to dynamically move tom next page
            url = request.META.get('HTTP_REFERER')# it will store what is the url in page
            try:
                print('inside try block')
                query = requests.utils.urlParse(url).query
                print('url',query)
                return redirect('dashboard')
            except:
                pass
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                print('url',query)
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)                
            except:
                return redirect('dashboard')
        else:
            messages.error(request,'invalid login credentials')
            return redirect('login')
    return render(request,'accounts/login.html')
@login_required(login_url = 'login')#if any user comes without loggedin it should redirect to there 
def logout(request):    
    auth.logout(request)
    messages.success(request,'you are logged out')
    return redirect('login')
def activate(request,uidb64,token):#upto this we have have encoded the uidb and token now we required to decode and seeting user status to is active if we click this link it will expire automatically again user wants again he need to set
    try:
        uid = urlsafe_base64_decode(uidb64).decode()# we are decoding by taking uidb64 give us pk of the user
        user = Account._default_manager.get(pk=uid)#getting the user
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):# is any of these error comes we are throwing user to none
        user = None

    if user is not None and default_token_generator.check_token(user, token):#user is not None there is a user and  we are getting token and if all those passes we are setting usser to is_active
        user.is_active = True 
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')
@login_required(login_url = 'login')
def dashboard(request):
    return render(request,'accounts/dashboard.html')

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():#if the user email exists
            user = Account.objects.get(email__exact = email) #if the user is typing exact mail what he have mentioned exact means casesensitive iexact means case insensitive
            #forgot password activation
            current_site = get_current_site(request)#getting localhost site
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),#are doing primary key encoding with this work so,no body can see this userid
                'token':default_token_generator.make_token(user),#we are declaring for this user and making a token for that partiular user
            })
            to_email = email#we are getting mail for user which is specifying
            send_email = EmailMessage(mail_subject,message,to = [to_email])#we are sending with these details
            send_email.send()
            messages.success(request,'password reset email has been sent to your email address ')
            return redirect('login')
        else:
            messages.error(request,'Account does not exist')
            return redirect('forgotpassword')

    return render(request,'accounts/forgotpassword.html')
def forgotpassword_email(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()# we are decoding by taking uidb64 give us pk of the user
        user = Account._default_manager.get(pk=uid)#getting the user
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):# is any of these error comes we are throwing user to none
        user = None

    if user is not None and default_token_generator.check_token(user, token):#user is not None there is a user and  we are getting token and if all those passes we are setting usser to is_active
        request.session['uid'] = uid
        messages.success(request,'please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request,'this link has been expired')
        return redirect('login')

def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk = uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Reset password successfully done')
            return redirect('login')
        else:
            messages.error(request,'passwords not match')
            return redirect('resetpassword')
    else:
        return render(request,'accounts/resetpassword.html')