from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render
from django.utils.html import format_html
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from .models import ContactMessage, FoodItem, Order
from django.utils.dateparse import parse_date

# Register FoodItem normally
admin.site.register(FoodItem)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'item', 'quantity', 'order_time', 'view_receipt')
    list_filter = ('order_time', 'payment_status')
    search_fields = ('customer_name', 'phone', 'item__name')
    change_list_template = "admin/orders/order/change_list.html"

    def view_receipt(self, obj):
        url = reverse('receipt', args=[obj.id])
        return format_html('<a class="button" href="{}" target="_blank">Print Receipt</a>', url)

    view_receipt.short_description = 'Receipt'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sales-report/', self.admin_site.admin_view(self.sales_report_view), name='sales-report'),
            path('sales-report/pdf/', self.admin_site.admin_view(self.sales_report_pdf_view), name='sales-report-pdf'),
        ]
        return custom_urls + urls

    def sales_report_view(self, request):
        orders = Order.objects.select_related('item').all().order_by('-order_time')

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        food_item = request.GET.get('food_item')
        payment_status = request.GET.get('payment_status')

        if start_date:
            orders = orders.filter(order_time__date__gte=parse_date(start_date))
        if end_date:
            orders = orders.filter(order_time__date__lte=parse_date(end_date))
        if food_item:
            orders = orders.filter(item__name=food_item)
        if payment_status and payment_status != 'All':
            orders = orders.filter(payment_status=payment_status)

        total_sales = sum(order.quantity * order.item.price for order in orders)
        total_orders = orders.count()

        for order in orders:
            order.computed_amount = order.quantity * order.item.price

        food_items = FoodItem.objects.all().order_by('name')

        # Define payment status options - adjust based on your model choices if different
        payment_status_choices = ['All', 'Pending', 'Paid', 'Failed']

        return render(request, 'admin/orders/order/sales_report.html', {
            'orders': orders,
            'total_sales': total_sales,
            'total_orders': total_orders,
            'start_date': start_date,
            'end_date': end_date,
            'selected_item': food_item,
            'selected_payment_status': payment_status if payment_status else 'All',
            'food_items': food_items,
            'payment_status_choices': payment_status_choices,
            'opts': self.model._meta,
        })

    def sales_report_pdf_view(self, request):
        orders = Order.objects.select_related('item').all().order_by('-order_time')

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        food_item = request.GET.get('food_item')
        payment_status = request.GET.get('payment_status')

        parsed_start = parse_date(start_date) if start_date else None
        parsed_end = parse_date(end_date) if end_date else None

        if parsed_start:
            orders = orders.filter(order_time__date__gte=parsed_start)
        if parsed_end:
            orders = orders.filter(order_time__date__lte=parsed_end)
        if food_item:
            orders = orders.filter(item__name=food_item)
        if payment_status and payment_status != 'All':
            orders = orders.filter(payment_status=payment_status)

        total_sales = sum(order.quantity * order.item.price for order in orders)

        for order in orders:
            order.computed_amount = order.quantity * order.item.price

        template = get_template('admin/orders/order/sales_report_pdf.html')
        html = template.render({
            'orders': orders,
            'total_sales': total_sales,
            'start_date': parsed_start,
            'end_date': parsed_end,
            'selected_item': food_item,
            'selected_payment_status': payment_status if payment_status else 'All',
        })

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Error generating PDF', status=500)
        return response


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'sent_at')
    search_fields = ('name', 'email', 'message')
