from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Item, OrderItem, Order
# Create your views here.

class HomeView(ListView):
    model = Item
    paginate_by = 4
    template_name = 'index.html'

class OrderView(DetailView):
    model = Order
    template_name = 'summary.html'



class ProductDetails(DetailView):
    model = Item
    template_name = "product.html"

def checkout(request):

    return render(request, 'checkout.html', {})

def add_to_cart(request, slug):
    
    if request.user.is_authenticated == False:
        messages.error(request, 'You must sign in to add an item to cart')
        return redirect('myapp:product',slug=slug)

    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            o = order.items.get(item__slug=item.slug)
            o.quantity += 1
            o.save()
            messages.info(request, 'Item has been added to cart')
             
        else:
            order_item = OrderItem.objects.create(item=item, user=request.user, ordered=False)
            order.items.add(order_item)
            messages.info(request, 'Item has been added to cart')

    else:
        order_item = OrderItem.objects.create(item=item, user=request.user, ordered=False)
        order = Order.objects.create(user=request.user)
        order.items.add(order_item)
        messages.info(request, 'Order created. Item added to cart.')
        
        
    return redirect('myapp:product',slug=slug)


def remove_from_cart(request, slug):

    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(user=request.user, item=item, ordered=False).exists():
            o = order.items.get(user=request.user, item=item, ordered=False)
            if o.quantity > 1:
                o.quantity -= 1
                o.save()
            else:
                order.items.filter(user=request.user, item=item, ordered=False).delete()
            messages.info(request, 'Item has been removed from cart')
            return redirect('myapp:summary', pk=order.id)
        else:
            messages.info(request, 'Item is not in cart')
            return redirect('myapp:summary', pk=order.id)
    
    else:
        messages.info(request, 'Order has not been created')
        return redirect('myapp:home')


