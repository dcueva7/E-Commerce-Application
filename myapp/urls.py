from . import views
from django.urls import path

app_name = 'myapp'

urlpatterns = [
    path('home/',views.home, name='home'),
    path('product/', views.product, name='product'),
    path('checkout/', views.checkout, name='checkout'),
]