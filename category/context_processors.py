'''
we will be using python function called context_processors
it takes request as an argumentand it will return dictonary of data/context
'''
from .models import Category
def menu_links(request):
    links = Category.objects.all()# it eill get all the categories
    return dict(links = links)