import uuid
from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from localflavor.us.models import USStateField, USZipCodeField

# Create your models here.

CATEGORY_CHOICES = [
    ('S', 'Tops'),
    ('B', 'Bottoms'),
    ('O', 'Outwear'),
]

LABEL_CHOICES = [
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger'),
]


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    discount = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
    file_name = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    

    def total_price_calc(self):
        return self.quantity*self.item.price 
    
    def get_discount_price(self):
        return self.item.discount*self.quantity 

    def __str__(self):
        return f'{self.quantity} {self.item.title}'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    f_name = models.CharField(max_length=50, null=True)
    l_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=200, null=True)
    address = models.CharField(max_length=500, null=True)
    address2 = models.CharField(max_length=200, null=True)
    country = CountryField()
    state = USStateField()
    zip = USZipCodeField()

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for item in self.items.all():
            if item.item.discount:
                total += item.get_discount_price()
            else:
                total += item.total_price_calc()

        return total
    
    def get_quantity(self):
        count = 0
        for item in self.items.all():
                count += item.quantity

        return count
