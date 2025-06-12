from django.contrib import admin
from .models import ContactMessage
from .models import FoodItem, Order

admin.site.register(FoodItem)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'item', 'quantity', 'order_time')
    list_filter = ('order_time',)
    search_fields = ('customer_name', 'phone', 'item__name')



@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'sent_at')
    search_fields = ('name', 'email', 'message')
