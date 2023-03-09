from . import views
from django.urls import path

app_name = 'myapp'

urlpatterns = [
    path('home/',views.HomeView.as_view(), name='home'),
    path('product/<slug>/', views.ProductDetails.as_view(), name='product'),
    path('checkout/', views.checkout, name='checkout'),
]