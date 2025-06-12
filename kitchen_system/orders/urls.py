from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('kitchen/', views.kitchen_view, name='kitchen'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('place_order/', views.place_order, name='place_order'),
    path('receipt/<int:order_id>/', views.receipt_view, name='receipt'),
    path('process_payment/<int:order_id>/', views.process_payment, name='process_payment'),
]
