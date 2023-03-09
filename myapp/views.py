from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Item
# Create your views here.

class HomeView(ListView):
    model = Item
    template_name = 'index.html'


class ProductDetails(DetailView):
    model = Item
    template_name = "product.html"
    



def checkout(request):

    return render(request, 'checkout.html', {})