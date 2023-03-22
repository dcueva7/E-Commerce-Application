from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from .models import Item, OrderItem, Order
from square.client import Client
import uuid
from django.views.generic.edit import UpdateView
from .forms import CheckoutForm
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

class CheckoutView(View):
    
    def get(self, *args, **kwargs):    
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'checkout.html', context)  
    


    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            return redirect('myapp:payment')


class ConfirmationView(DetailView):
    model = Order
    template_name = 'confirmation.html'
    

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


def handle_payment(request, id):

    order = Order.objects.get(user=request.user, ordered=False)

    client = Client(
    access_token= 'EAAAEI3TGNvdL52SiVss0nEBL9BIi1Cg_COppPNbjfNez6y7_Vjn2xGVjBRbOORu',
    environment='sandbox')

    amount = 100*(int(order.get_total())) 

    result = client.payments.create_payment(
        body = {
            "source_id": id, 
            "idempotency_key": str(uuid.uuid4()),
            "amount_money": {
            "amount": amount, 
            "currency": "USD"
            },
        }
    )

    if result.is_success():
        print(result.body)
    
    elif result.is_error():
        print(result.errors)

    return redirect('myapp:confirmation', pk=order.id)

def payment_view(request):

    return render(request, 'payment.html')
