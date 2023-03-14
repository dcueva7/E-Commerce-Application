from django import template
from myapp.models import Order

register = template.Library()

@register.filter 
def item_count(user):
    if user.is_authenticated:
        order_qs = Order.objects.filter(user=user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            return order.items.count()
        
    return 0

@register.filter
def order_pk(user):
    if user.is_authenticated:
        order_qs = Order.objects.filter(user=user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            return order.id
        
    return 0
    

