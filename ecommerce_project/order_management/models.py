from django.db import models
from products.models import Product
from custom_authentication.models import CustomUser
# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ShoppingCart(BaseModel):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.id}'


    def __repr__(self) -> str:
        return f'CART_ID:{self.id}-USER_ID:{self.user_id}-PRODUCT_ID:{self.product_id}'


class Order(BaseModel):
    ORDER_STATUS = [
        ("pending", "Pending"),
        ("failed", "Failed"),
        ("success", "Success"),
    ]
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="pending")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self) -> str:
        return f'{self.id}'


    def __repr__(self) -> str:
        return f'ID:{self.id}-ORDER_STATUS:{self.status}'


class OrderLineItems(BaseModel):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.PROTECT)
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.id}'


    def __repr__(self) -> str:
        return f'ORDER_LINE_ITEM_ID:{self.id}-ORDER_ID:{self.order_id}-PRODUCT_ID:{self.product_id}'


class Inventory(BaseModel):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.id}'


    def __repr__(self) -> str:
        return f'INVENTORY_ID:{self.id}-PRODUCT_ID:{self.product_id}-QUANTITY:{self.quantity}'

