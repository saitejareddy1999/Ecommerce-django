from django.shortcuts import render,redirect
from .forms import RegistrationForm
from accounts.models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

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
            auth.login(request,user)
            messages.success(request,'you are logged in')
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