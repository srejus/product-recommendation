from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from product.models import Product
from product.serializers import ProductSerailizer
from . utils import recommend_products

# Create your views here.
class RecommendationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request,id):
        product = Product.objects.filter(id=id)
        if not product.exists():
            return Response({"status":"failed","message":"No Product found with the given id"},status=status.HTTP_404_NOT_FOUND)
        
        try:
            result = recommend_products(product.first())
        except ValueError as e:
            return Response({"status":"failed","message":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
        recommended_products_ids = [product.id for product in result]
        recommended_products = Product.objects.filter(id__in=recommended_products_ids)
        serializer = ProductSerailizer(instance=recommended_products,many=True)
        return Response({"status":"success","message":"Data fetched successfully","data":serializer.data},status=status.HTTP_200_OK)
