from django.db import models
from django.utils import timezone

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.CharField(max_length=255)  # store image filename or URL

    def __str__(self):
        return self.name

class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    ]

    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_time = models.DateTimeField(auto_now_add=True)

    amount_paid = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    payment_time = models.DateTimeField(null=True, blank=True)

    mpesa_code = models.CharField(max_length=20, blank=True, null=True)  # New field for M-Pesa code

    def __str__(self):
        return f"Order for {self.customer_name} - {self.item.name}"



class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"