from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    price           = models.IntegerField()
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)#foreignkey--> on_delete=models.CASCADE-->if the category is deleted related products also should be deleted
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    def get_url(self):
        return reverse('product_detail',args = [self.category.slug,self.slug])#self is pointing current class object and category is present in product and in that category we have slug so here we have foreignkey relationship so it will combine both
    def __str__(self):
        return self.product_name
class VariationManager(models.Manager):#this for differentiate b/w colors and sizes if we keep only set_all it will just gives all names for respective products
    def colors(self):
        return super(VariationManager,self).filter(variation_category = 'color',is_active =True)
    def sizes(self):
        return super(VariationManager,self).filter(variation_category = 'size',is_active =True)
variation_category_choice = (('color','color'),('size','size'))
class Variation(models.Model):
    product            = models.ForeignKey(Product,on_delete = models.CASCADE)#we are going to add variation of particular product
    variation_category = models.CharField(max_length=100,choices = variation_category_choice)
    variation_value    = models.CharField(max_length=100)
    is_active          = models.BooleanField(default=True)#if u want to disable any variation value
    created_date       = models.DateTimeField(auto_now=True) 
    objects            = VariationManager()#to include what it is doing
    def __str__(self):
        return self.variation_value