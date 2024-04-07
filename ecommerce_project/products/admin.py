from django.contrib import admin

# Register your models here.
from .models import Product, Category, ProductCategory

admin.site.register([Product,Category,ProductCategory])
