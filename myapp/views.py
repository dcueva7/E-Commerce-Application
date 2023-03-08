from django.shortcuts import render
from .models import Item
# Create your views here.

def home(request):
    context = {
        'items': Item.objects.all()
    }
    
    return render(request, "index.html", context)
    

def product(request):

    return render(request, 'product.html', {})


def checkout(request):

    return render(request, 'checkout.html', {})