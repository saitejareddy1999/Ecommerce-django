from django.db import models
from store.models import Product,Variation

# Create your models here.
class Cart(models.Model):
    cart_id    = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):#to override the object name of the class
        return self.cart_id
    
class CartItem(models.Model):#to specify one page cartitem
    '''
    we have to add variation from add cart all poducts variation so here we don't have specific database so we required to add '''
    product      = models.ForeignKey(Product,on_delete=models.CASCADE)
    variations    = models.ManyToManyField(Variation,blank =True) #so here we can have many products can have same variations same product can have with new variation handle that situation also
    cart         = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity     = models.IntegerField()
    is_active    = models.BooleanField(default = True)
    def sub_total(self):#we have to caluclate sepearate price here
        return self.product.price * self.quantity
    def __unicode__(self):
        return self.product
