from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account,UserProfile
from django.utils.html import format_html

'''
this for creating custom user model for if we dont want any project in default admin page as django admin page we are required to create custom admin page in accounts in  any web page they are not going to login with username and password we are required to create email and password as login for user. 
'''
# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email','first_name','last_name', 'username','last_login','date_joined','is_active')
    list_display_links = ('email','first_name','last_name')
    readonly_fields = ('last_login','date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
# class UserProfileAdmin(admin.ModelAdmin):
#     def thumbnail(self,object):
#         return format_html('<img src = "{}" width ="30" style="border-radius:50%">'.format(object.profile_picture.url))
#     thumbnail.short_description = 'profile picture'
#     list_display =('thumbnail','user','state','country')
# admin.site.register(Account,AccountAdmin)
# admin.site.register(UserProfile,UserProfileAdmin)
class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%">'.format(object.profile_picture.url))
    thumbnail.short_description = 'profile picture'
    list_display = ('thumbnail', 'user', 'state', 'country')

admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)



'''
if we add accountadmin to register site it will not allow which is created all the fields in django
    filter_horizontal = ()
    list_filter = ()
to clickable fields is only email but we need to clickable two more fields list_display_links = ('email','first_name','last_name') using this command
which should come first=we can keep - there in front
password to set readonly fieldsets= ()
'''