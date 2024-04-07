from django.contrib import admin

# Register your models here.
from .models import ShoppingCart,Order,OrderLineItems,Inventory

admin.site.register([ShoppingCart,Order,OrderLineItems,Inventory])
