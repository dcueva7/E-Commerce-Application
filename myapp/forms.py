from django import forms
from .models import Order


class CheckoutForm(forms.Form):
    class Meta:
        model = Order
        fields = ['f_name', 'l_name', 'email', 'address', 'address2', 'country', 'state', 'zip']
    
