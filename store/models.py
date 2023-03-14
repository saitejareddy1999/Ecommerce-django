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
