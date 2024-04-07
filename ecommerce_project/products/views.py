# Create your views here.

from rest_framework import permissions
from .models import Product
from .serializers import ProductSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import Product, ProductCategory, Category
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs) -> Response:
        data = Product.objects.all().values()
        return Response(data)

    def retrieve(self, request, *args, **kwargs) -> Response:
        data = Product.objects.filter(id=kwargs['pk']).values()
        #NOTE: should have returned dict instead of list of dict
        return Response(data)

    def create(self, request, *args, **kwargs) -> Response:
        product_serializer_data = ProductSerializer(data=request.data)
        if product_serializer_data.is_valid():
            product_serializer_data.save()
            status_code = status.HTTP_201_CREATED
            return Response({"message": "Product Added Sucessfully", "status": status_code})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "please fill the datails", "status": status_code})

    def destroy(self, request, *args, **kwargs) -> Response:
        product_data = Product.objects.get(id=kwargs['pk'])
        if product_data:
            product_data.active = False
            product_data.save()
            status_code = status.HTTP_201_CREATED
            return Response({"message": "Product deactivated Sucessfully", "status": status_code})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Product data not found", "status": status_code})

    def update(self, request, *args, **kwargs) -> Response:
        product_details = Product.objects.get(id=kwargs['pk'])
        product_serializer_data = ProductSerializer(
            product_details, data=request.data, partial=True)
        if product_serializer_data.is_valid():
            product_serializer_data.save()
            status_code = status.HTTP_201_CREATED
            return Response({"message": "Product Update Sucessfully", "status": status_code})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Product data Not found", "status": status_code})