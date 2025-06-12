from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render
from django.utils.html import format_html
from django.db.models import Sum
from .models import ContactMessage, FoodItem, Order

# Register FoodItem normally
admin.site.register(FoodItem)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'item', 'quantity', 'order_time', 'view_receipt')  # Added view_receipt
    list_filter = ('order_time',)
    search_fields = ('customer_name', 'phone', 'item__name')
    change_list_template = "admin/orders/order/change_list.html"  # Custom changelist template

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sales-report/', self.admin_site.admin_view(self.sales_report_view), name='sales-report'),
        ]
        return custom_urls + urls

    def sales_report_view(self, request):
        orders = Order.objects.all()
        total_sales = sum(order.quantity * order.item.price for order in orders)

        for order in orders:
            order.computed_amount = order.quantity * order.item.price

        return render(request, 'admin/orders/order/sales_report.html', {
            'orders': orders,
            'total_sales': total_sales,
            'opts': self.model._meta,
        })

    def view_receipt(self, obj):
        url = reverse('receipt', args=[obj.id])
        return format_html('<a class="button" href="{}" target="_blank">Print Receipt</a>', url)

    view_receipt.short_description = 'Receipt'
    view_receipt.allow_tags = True


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'sent_at')
    search_fields = ('name', 'email', 'message')
