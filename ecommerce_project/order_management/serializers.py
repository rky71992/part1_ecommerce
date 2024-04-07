from rest_framework import serializers
from .models import ShoppingCart

class ShoppingCartModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ['id', 'user_id', 'product', 'quantity']

class ShoppingCartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class ShoppingCartSerializer(serializers.Serializer):
    products = ShoppingCartItemSerializer(many=True)

class InventoryUpdateItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class InventoryUpdateSerializer(serializers.Serializer):
    products = ShoppingCartItemSerializer(many=True)