# your_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('kitchen/', views.kitchen_view, name='kitchen'),
    path('about/', views.about_view, name='about'),  # <-- add this if missing
    path('contact/', views.contact_view, name='contact'),  # same for contact
    path('place_order/', views.place_order, name='place_order'),
    path('receipt/<int:order_id>/', views.receipt_view, name='receipt'),

]

