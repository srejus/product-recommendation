import requests

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from . models import Product
from . serializers import ProductSerailizer


# Create your views here.
class PopulateProductView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        queryset = Product.objects.all()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = ProductSerailizer(instance=paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self,request):
        if Product.objects.all().exists():
            return Response({"status":"failed","message":"You already imported all products from the api"}
                            ,status=status.HTTP_400_BAD_REQUEST)
        
        url = 'https://dummyjson.com/products'
        response = requests.request("GET", url, headers={}, data={})
        if response.status_code == 200:
            serializer = ProductSerailizer(data=response.json().get('products',[]),many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response({"status":"success","message":f"Products imported successfully from {url}"}
                            ,status=status.HTTP_201_CREATED)
        
        return Response({"status":"failed","message":f"Error occured while saving the data {response.text}"},status=status.HTTP_400_BAD_REQUEST)
    

class ProductView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    
    def get(self,request,id=None):
        queryset = Product.objects.all()
        if id:
            queryset = queryset.filter(id=id)
            if not queryset.exists():
                return Response({"status":"failed","message":"No product found with the given id"},status=status.HTTP_404_NOT_FOUND)
            serializer = ProductSerailizer(instance=queryset.first(),many=False)
            return Response({"status":"success","message":"Data fetched successfully","data":serializer.data},status=status.HTTP_200_OK)
        
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = ProductSerailizer(instance=paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
