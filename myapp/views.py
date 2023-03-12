from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView
from .models import Item, OrderItem, Order
# Create your views here.

class HomeView(ListView):
    model = Item
    template_name = 'index.html'


class ProductDetails(DetailView):
    model = Item
    template_name = "product.html"

def checkout(request):

    return render(request, 'checkout.html', {})

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            o = order.items.get(item__slug=item.slug)
            o.quantity += 1
            o.save()
             
        else:
            order_item = OrderItem.objects.create(item=item)
            order.items.add(order_item)

    else:
        order_item = OrderItem.objects.create(item=item)
        order = Order.objects.create(user=request.user)
        order.items.add(order_item)
        

        
        
    return redirect('myapp:product',slug=slug)

    

