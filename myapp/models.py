
from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.

CATEGORY_CHOICES = [
        ('S','Shirt'),
        ('SW','Sportwear'),
        ('O','Outwear'),
]

LABEL_CHOICES = [
        ('P','primary'),
        ('S','secondary'),
        ('D','danger'),
]

class Item(models.Model):
        title = models.CharField(max_length=100)
        price = models.DecimalField(decimal_places=2, max_digits=10)
        discount = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
        category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
        label = models.CharField(choices=LABEL_CHOICES, max_length=1)
        slug = models.SlugField()
        description = models.TextField()
       

        def __str__(self):
                return self.title
        


class OrderItem(models.Model):
        item = models.ForeignKey(Item, on_delete=models.CASCADE)
        quantity = models.IntegerField(default=1)

        def __str__(self):
                return self.title


class Order(models.Model):
        user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        ordered = models.BooleanField(default=False)
        items = models.ManyToManyField(OrderItem)
        start_date = models.DateTimeField(auto_now_add=True)
        ordered_date = models.DateTimeField()


        def __str__(self):
                return self.user.username
