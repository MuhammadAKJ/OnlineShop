from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..shop.models import Product
from .serializers import ProductSerializer

from rest_framework_simplejwt.authentication import JWTAuthentication
from permissions import IsOwner
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class ProductListApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, *args, **kwargs):

        products = Product.objects.filter(name = request.user.name)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



    def post(self, request, *args, **kwargs):
        data = {
             'category' : request.data.get('category'),
             'name' : request.data.get('name'),
             'slug' : request.data.get('slug'),
             'image' : request.data.get('image'),
             'description': request.data.get('description'),
             'price' : request.data.get('price'),
             'available' : request.data.get('available')
        }
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self, name, slug):
        """
        Get object with given name and slug
        """
        try:
            return Product.objects.get(name=name, slug=slug)
        except Product.DoesNotExist:
            return None

    def get(self, request, name, slug, *args, **kwargs):
        """
        Retrievs the product with given name
        """
        product_instance = self.get_object(name, slug)
        if not product_instance:
            return Response(
                {"res":"Object with name does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ProductSerializer(product_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, name, slug):
        """
        Update the products
        """
        product_instance = self.get_object(name, slug)
        if not product_instance:
            return Response(
                {"res": "Object with name does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'name': request.data.get('name'),
            'slug': request.data.get('slug'),
            'price': request.data.get('price'),
            'available': request.data.get('available'),
            'description': request.data.get('description')
        }
        serializer = ProductSerializer(instance=product_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name, slug):
        """
        Deletes the product
        """
        product_instance = self.get_object(name, slug)
        if not product_instance:
            return Response(
                {"res":"Object with name does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        product_instance.delete()
        return Response(
            {"res": "Product deleted"},
            status=status.HTTP_200_OK
        )