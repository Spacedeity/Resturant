from django.shortcuts import render, redirect, get_object_or_404

from .models import ContactMessage
from django.contrib import messages
from .models import FoodItem, Order
from itertools import islice
from django.utils import timezone

def chunked(iterable, size):
    iterable = iter(iterable)
    return iter(lambda: list(islice(iterable, size)), [])

def kitchen_view(request):
    items = FoodItem.objects.all()
    chunked_items = chunked(items, 5)  # group items 5 per section
    return render(request, 'orders/kitchen.html', {'sections': chunked_items})

def home(request):
    return render(request, 'orders/index.html')

def about_view(request):
    return render(request, 'orders/about.html')


def place_order(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        phone = request.POST.get('phone')
        quantity = int(request.POST.get('quantity', 1))
        item_id = request.POST.get('item_id')

        try:
            food_item = FoodItem.objects.get(id=item_id)

            # Create order with initial payment status
            order = Order.objects.create(
                customer_name=customer_name,
                phone=phone,
                quantity=quantity,
                item=food_item,
                amount_paid=None,
                payment_status='Pending',
                payment_time=None,
                mpesa_code=''  # initialize blank mpesa_code field
            )

            return redirect('receipt', order_id=order.id)

        except FoodItem.DoesNotExist:
            return render(request, 'orders/receipt.html', {'error': 'Food item not found'})

    # For GET or other methods:
    return render(request, 'orders/receipt.html', {'error': 'Invalid request method'})

def receipt_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    total_price = order.quantity * order.item.price
    return render(request, 'orders/receipt.html', {
        'order': order,
        'total_price': total_price,
    })

def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        mpesa_code = request.POST.get('mpesa_code', '').strip().upper()

        if mpesa_code:
            # Basic validation for M-Pesa code length
            if not (10 <= len(mpesa_code) <= 20):
                return render(request, 'orders/receipt.html', {
                    'order': order,
                    'total_price': order.quantity * order.item.price,
                    'error': 'M-Pesa code must be between 10 and 20 characters.'
                })

            # Save payment details
            order.mpesa_code = mpesa_code
            order.payment_status = 'Paid'
            order.payment_time = timezone.now()
            order.save()

            return redirect('receipt', order_id=order.id)

        else:
            return render(request, 'orders/receipt.html', {
                'order': order,
                'total_price': order.quantity * order.item.price,
                'error': 'M-Pesa code is required.'
            })

    # For GET or other methods, redirect back to receipt page
    return redirect('receipt', order_id=order.id)



def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Save to the database
        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )

        # Optional: add a success message to show in the template
        messages.success(request, 'Your message has been sent successfully.')
        return redirect('contact')  # Reload page after POST

    return render(request, 'orders/contact.html')
