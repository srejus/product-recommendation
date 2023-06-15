from rest_framework import serializers

from product.models import Product
from . models import Order,OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        depth = 1
    
    def validate(self,data):
        product = self.initial_data.get('product')
        quantity = int(data.get('quantity','1'))
        if quantity < 1:
            raise serializers.ValidationError({"quantity":"This field must be atleast 1"})
        product_instance = Product.objects.filter(id=product)
        try:
            if product and not product_instance.exists():
                raise serializers.ValidationError({"product":"No product found"})
        except ValueError:
            raise serializers.ValidationError({"product":"product must be a valid integer"})
    
        data['product'] = product_instance.first()
        data['price'] = product_instance.first().price*quantity
        return data

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['customer']
    

    def validate(self,data):
        errors = []
        order_items = self.initial_data.get('order_items')
        rating = self.initial_data.get('rating')
        
        if not order_items:
            errors.append({"order_items":"This field is requried"})
        
        if not rating:
            errors.append({"rating":"This field is requried"})
        
        if rating and rating > 5.0 or rating < 0.0:
            errors.append({"rating":"This field must be between 1.00 and 5.00"})
            
        if errors:
            raise serializers.ValidationError({"errors":errors})
        
        data['order_items'] = order_items
        return data

    def create(self, validated_data):
        order_items = validated_data.pop('order_items',[])
        instance = Order.objects.create(customer=self.initial_data.get('customer'),**validated_data)
        total_amount = 0
        
        '''
        In real world scenario we need to check if the order_items is valid or not before saving the order instance
        and if the order_items is invalid then we need to return error message instead of saving the order instance.
        
        Since the project is not for creating order I just skipped that and create the order instance first then checking
        order_items are valid or not
        '''
        for order_item in order_items:
            order_item_serializer = OrderItemSerializer(data=order_item)
            order_item_serializer.is_valid(raise_exception=True)
            order_item_instance = order_item_serializer.save(order=instance)
            total_amount += order_item_instance.price
        
        instance.total_amount = total_amount
        instance.save()
        return instance


class OrderViewSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = '__all__'
    
    def get_order_items(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        order_item_serializer = OrderItemSerializer(order_items, many=True)
        return order_item_serializer.data

        
    

        