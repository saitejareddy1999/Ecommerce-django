from django import forms
from .models import Account,UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput(attrs={
        'placeholder':'Enter password',
         #instead of specifying this class field in all the feilds which are present in html page we require lot of space to coding instead of that we are required do take a functon and create for feilds one time only
        }))
    confirm_password = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder':'confirm password'}))
    class Meta:
        model = Account
        fields = ['first_name','last_name','email','phone_number','password']
    def clean(self):
        cleaned_data = super(RegistrationForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(('password does not match!!...'))

    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phonenumber'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control' 
class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name','last_name','email','phone_number']
        def __init__(self,*args,**kwargs):
            super(UserForm,self).__init__(*args,**kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control'  
class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required = False,error_messages = {'invalid' : {"image fields only"}},widget = forms.FileInput)#writtten ths  for in forms page to not visible
    class Meta:
        model = UserProfile
        fields = ['address_line_1',"address_line_2","profile_picture","city","state","country"]
        def __init__(self,*args,**kwargs):
            super(UserProfileForm,self).__init__(*args,**kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs['class'] = 'form-control' 


