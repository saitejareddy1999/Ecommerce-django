from django.urls import path#we are cretaing here urls.py because if we create in multiple urls.py in one file it may cause maintainence problems so that we are creating sepearatly in app folder 
from . import views

urlpatterns = [
    path('',views.store,name='store'),
    path('category/<slug:category_slug>/',views.store,name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',views.product_detail,name='product_detail'),
    path('search/',views.search,name='search'),
    
]
