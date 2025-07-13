# cart/urls.py
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/', views.cart_add, name='cart_add'),
    path('remove/<int:variant_id>/', views.cart_remove, name='cart_remove'),
    path('update/<int:variant_id>/', views.cart_update, name='cart_update'),
    # We will add a URL for updating quantities later
    # path('update/<int:variant_id>/', views.cart_update, name='cart_update'),
]