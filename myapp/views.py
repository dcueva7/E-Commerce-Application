from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from .models import Item, OrderItem, Order
from square.client import Client
import uuid
from datetime import datetime
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
            'form': form, 'order': Order.objects.get(user=self.request.user, ordered=False)
        }
        return render(self.request, 'checkout.html', context)  
    


    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            first = form.cleaned_data.get('f_name')
            last = form.cleaned_data.get('l_name')
            email = form.cleaned_data.get('email')
            address = form.cleaned_data.get('address')
            address2 = form.cleaned_data.get('address2')
            city = form.cleaned_data.get('city')
            country = form.cleaned_data.get('country')
            state = form.cleaned_data.get('state')
            zip = form.cleaned_data.get('zip')
            Order.objects.filter(user=self.request.user, ordered=False).update(f_name=first, l_name=last, email=email, address=address, address2=address2,city=city, country=country, state=state, zip=zip)
            return redirect('myapp:payment')
        else:
            messages.warning(self.request, 'Invalid form submission')


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
        if order.items.filter(item__slug=item.slug, ordered=False).exists():
            o = order.items.get(item__slug=item.slug, ordered=False)
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
        order.ordered = True
        order.save()
        order.ordered_date = datetime.now()
        order.save()
        for i in order.items.all():
            i.ordered = True
            i.save()
    
    elif result.is_error():
        print(result.errors)

    return redirect('myapp:confirmation', pk=order.id)

def payment_view(request):
    
    context = {
        'order': Order.objects.get(user=request.user, ordered=False)
    }

    return render(request, 'payment.html', context)
