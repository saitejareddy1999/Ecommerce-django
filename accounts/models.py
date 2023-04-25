from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
'''
we are creating our own login page instead of taking it from django and also creating superuser model
'''
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password = None):#this is for creating user
        if not email:
            raise ValueError('user must have an email address')
        if not username:
            raise ValueError('user must have an username')
        user = self.model(#that actually refers back to the SomeModel class
            email = self.normalize_email(email),#if u enter capital letter email adress it will automatically does small letter
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    def create_superuser(self, first_name, last_name, email, username, password ):#this is for creating superuser
        user = self.create_user(
            email = self.normalize_email(email),#if u enter capital letter email adress it will automatically does small letter
            username = username,
            password = password,
            first_name = first_name,
            last_name =last_name,
            
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using = self._db)
        return user


# Create your models here.
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique = True)
    email = models.EmailField(max_length = 50,unique = True)
    phone_number = models.CharField(max_length = 50)

    #required
    date_joined = models.DateTimeField(auto_now_add = True)
    last_login = models.DateTimeField(auto_now_add = True)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = False)
    is_superadmin = models.BooleanField(default = False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = MyAccountManager()#while creating account u need to say create user and superuser
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    def __str__(self): #when we call account object it just returns the email
        return self.email
    def has_perm(self, perm, obj = None):#if the user is admin he has all the perm to edit and update the changes
        return self.is_admin
    def has_module_perms(self,add_label):
        return True

