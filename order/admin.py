from django.contrib import admin

from .models import Order,OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','customer','total_amount','rating','ordered_at']
    

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id','order','quantity','price','product']
    

# Register your models here.
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
