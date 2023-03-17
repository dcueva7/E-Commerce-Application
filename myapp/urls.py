from . import views
from django.urls import path

app_name = 'myapp'

urlpatterns = [
    path('',views.HomeView.as_view(), name='home'),
    path('product/<slug>/', views.ProductDetails.as_view(), name='product'),
    path('summary/<pk>/', views.OrderView.as_view(), name='summary'),
    path('checkout/<pk>', views.CheckoutView.as_view(), name='checkout'),
    path('add_to_cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    path('remove_from_cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),
    path('handle_payment/<str:id>/', views.handle_payment, name='handle'),
]