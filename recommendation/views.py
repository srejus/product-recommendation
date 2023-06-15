from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from product.models import Product
from product.serializers import ProductSerailizer
from order.models import OrderItem
from . utils import recommend_products,calculate_accuracy

# Create your views here.
class RecommendationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request,id):
        user = User.objects.filter(id=id)
        if not user.exists():
            return Response({"statius":"failed","message":"No User found with the given id"},status=status.HTTP_404_NOT_FOUND)
        
        try:
            result = recommend_products(user.first())
        except ValueError as e:
            return Response({"status":"failed","message":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
        actual_products = [item.product for item in OrderItem.objects.filter(order__customer=user.first())]

        accuracy = calculate_accuracy(actual_products, result)

        recommended_products_ids = [product.id for product in result]
        recommended_products = Product.objects.filter(id__in=recommended_products_ids)
        serializer = ProductSerailizer(instance=recommended_products,many=True)
        return Response({"status":"success","message":"Data fetched successfully","data":serializer.data,"accuracy":accuracy},status=status.HTTP_200_OK)
