from django.shortcuts import render
from django.http import JsonResponse
from .models import FoodItem, Order
from itertools import islice

def chunked(iterable, size):
    iterable = iter(iterable)
    return iter(lambda: list(islice(iterable, size)), [])

def kitchen_view(request):
    items = FoodItem.objects.all()
    chunked_items = chunked(items, 5)  # group items 5 per section
    return render(request, 'orders/kitchen.html', {'sections': chunked_items})
from django.shortcuts import redirect

def place_order(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        phone = request.POST.get('phone')
        quantity = int(request.POST.get('quantity', 1))
        item_id = request.POST.get('item_id')

        try:
            food_item = FoodItem.objects.get(id=item_id)
            order = Order.objects.create(
                customer_name=customer_name,
                phone=phone,
                quantity=quantity,
                item=food_item
            )
            return redirect('receipt', order_id=order.id)
        except FoodItem.DoesNotExist:
            return render(request, 'orders/receipt.html', {'error': 'Food item not found'})
    else:
        return render(request, 'orders/receipt.html', {'error': 'Invalid request method'})


def home(request):
    return render(request, 'orders/index.html')

def about_view(request):
    return render(request, 'orders/about.html')

def contact_view(request):
    return render(request, 'orders/contact.html')
    
from django.shortcuts import get_object_or_404

def receipt_view(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        return render(request, 'orders/receipt.html', {'order': order})
    except Order.DoesNotExist:
        return render(request, 'orders/receipt.html', {'error': 'Order not found'})
