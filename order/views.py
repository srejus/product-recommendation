import random

from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.pagination import LimitOffsetPagination

from product.models import Product
from .serializers import OrderSerializer,OrderViewSerializer


# Create your views here.
class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    
    def post(self,request):
        request.data['customer'] = request.user
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        instance = serializer.save()
        view_serializer = OrderViewSerializer(instance=instance)
        return Response({"status":"success","message":"Order created successfully","data":view_serializer.data},status=status.HTTP_201_CREATED)


class PopulateOrderView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    
    def post(self,request):
        no_of_orders = request.data.get('no_of_orders',10)
        
        try:
            if not no_of_orders.isnumeric():
                return Response({"status":"failed","message":"Invalid no_of_orders"},status=status.HTTP_400_BAD_REQUEST)
            no_of_orders = int(no_of_orders)
        except AttributeError:
            pass
        
        users = User.objects.all()
        users_list = [user for user in users]
        
        products = Product.objects.all()
        products_list = [product for product in products]
        
        for i in range(no_of_orders):
            product = random.choice(products_list)
            quantity = random.randint(1,5)
            data = {
                "order_items":[
                    {
                        "product":product.id,
                        "quantity":quantity,
                        "price":product.price*quantity
                    }
                ],
                "customer":random.choice(users_list)
            }
            
            
            serializer = OrderSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response({"status":"success","message":"Orders created successfully"})