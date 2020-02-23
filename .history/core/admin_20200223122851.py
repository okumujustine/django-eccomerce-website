from django.contrib import admin

from .models import  Item, Order, OrderItem, CheckoutForm
# Register your models here.

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CheckoutForm) 
