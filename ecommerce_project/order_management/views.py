# Create your views here.

from rest_framework import permissions
#from .models import Product
from .serializers import ShoppingCart
from django.db import transaction

from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import *
import random
from .serializers import*
# Create your views here.
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

class ShoppingCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs) ->Response:
        current_user = request.user
        cart_data = ShoppingCart.objects.filter(user_id=current_user).values()
        return Response([cart_data])

    def delete(self, request, *args, **kwargs) -> Response:
        #NOTE: should able to delete single product. current implementation abadons the cart
        current_user = request.user
        ShoppingCart.objects.filter(user_id=current_user).delete()
        status_code = status.HTTP_201_CREATED
        return Response({"message": "Cart Emptied delete Sucessfully", "status": status_code})
        
    def put(self, request, *args, **kwargs) ->Response:
        #NOTE: If some product is recieved, what shuld be done(Error and dont save anything/skip that  product)
        current_user = request.user
        serializer = ShoppingCartSerializer(data=request.data)
        if serializer.is_valid():
            cart_items = serializer.validated_data['products']
            for item in cart_items:
                #NOTE: only those products which are active can be added to th cart
                product_data = Product.objects.get(id=item['product_id'],active=True)
                #NOTE we need to add more logic to update the quantity of shipping cart 
                #product quantity if product already in the cart, instead of adding again
                if product_data and product_data.max_per_order >= item['quantity']:
                    cart_item = ShoppingCart.objects.create(user_id=current_user, product_id=product_data, quantity=item['quantity'])
                    cart_item.save()
            return Response({'message': 'Shopping cart items added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class OrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs) ->Response:
        current_user = request.user
        return Response([Order.objects.filter(user_id=current_user).values()])
        
    def post(self, request, *args, **kwargs) ->Response:
        current_user = request.user
        #NOTE: Assuming order place will have payment details
        #NOTE: We are assuming order will be transacted once
    
        shopping_cart_items = ShoppingCart.objects.filter(user_id=current_user).values()
        if not shopping_cart_items:
            return Response({'message': 'Add products to cart to place order'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            sid = transaction.savepoint()
            try:
                amount = 0
                for cart_item in shopping_cart_items:
                    amount += cart_item['quantity']*Product.objects.get(id=cart_item['product_id_id']).price

                new_order = Order.objects.create(user_id=current_user,status='pending',total_amount=amount)
                new_order.save()

                for cart_item in shopping_cart_items:
                    order_line_item = OrderLineItems.objects.create(
                        order_id=new_order,
                        product_id=Product.objects.get(id=cart_item['product_id_id']),
                        quantity=cart_item["quantity"]
                    )
                    order_line_item.save()
                
                for cart_item in shopping_cart_items:
                    product_inventory = Inventory.objects.get(id=cart_item['product_id_id'])
                    if product_inventory.quantity >= cart_item["quantity"]:
                        product_inventory.quantity -= cart_item["quantity"]
                        product_inventory.save()
                    else:
                        raise Exception(f"Insufficient inventory for product")

                #NOTE: assuming that transaction will randomly pass or fail
                transaction_status = random.choice([True, False])
                #transaction_status = True# for testing purpose
                if not transaction_status:
                    raise Exception(f"Transaction Failed")
                
                new_order.status = 'success'
                new_order.save()
                ShoppingCart.objects.filter(user_id=current_user).delete()
                
            except Exception as ex:
                transaction.savepoint_rollback(sid)
                raise ex
        return Response({'message': 'Order Places successfully'}, status=status.HTTP_201_CREATED)
    

class InventoryView(APIView):
    serializer_class = Order
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs) ->Response:
        return Response([Inventory.objects.filter().values()])
        
    def put(self, request, *args, **kwargs) ->Response:
        #NOTE: what to do if incorrect product_id is recieved, raise error or skip or return mesage
        serializer = InventoryUpdateSerializer(data=request.data)
        if serializer.is_valid():
            inventory_items = serializer.validated_data['products']
            for item in inventory_items:
                product_data = Product.objects.get(id=item['product_id'])
                if product_data:
                    product_inventory = Inventory.objects.get(product_id=product_data)
                    if product_inventory:
                        product_inventory.quantity += item['quantity']
                    else:
                        product_inventory = Inventory.objects.create(product_id=product_data,quantity=item['quantity'])
                    product_inventory.save()
        return Response({'message': 'Inventory Updated successfully'}, status=status.HTTP_201_CREATED)