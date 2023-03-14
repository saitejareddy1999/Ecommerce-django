from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name   = models.CharField(max_length=50, unique = True)
    slug            = models.SlugField(max_length=100, unique = True) # TO DEFINE URL FOR A CATEGORY THIS IS UNIQUE
    description     = models.TextField(max_length = 255, blank = True)#blank = True---optional--means It simply means that field can be empty
    cat_image       = models.ImageField(upload_to = 'photos/categorys',blank = True)
    '''
    It is the way to change the behavior of Django tables like table name, field order, field constraints, indexes,
    '''
    class Meta:#this is for if in admin page it is creating plural we don't want that we creating our own name
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    def get_url(self):
        return reverse('products_by_category',args = [self.slug])#it will take name of the category slug
    def __str__(self):
        return self.category_name

