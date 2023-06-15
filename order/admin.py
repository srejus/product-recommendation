from django.contrib import admin

from .models import Order,OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','customer','total_amount','ordered_at']
    

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id','order','quantity','price']
    

# Register your models here.
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
