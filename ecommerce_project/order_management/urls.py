from django.urls import path
from .views import ShoppingCartView, OrderView, InventoryView
#from snippets import views

urlpatterns = [
    path('cart/', ShoppingCartView.as_view(), name='shopping_cart'),
    path('order/', OrderView.as_view(), name='order_place'),
    path('inventory/', InventoryView.as_view(), name='product_inventory'),
]