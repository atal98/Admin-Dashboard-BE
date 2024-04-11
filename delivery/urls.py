from django.contrib import admin
from django.urls import path
from delivery.views import *

urlpatterns = [
    path('delivery_info/',
         DeliveryInfoAPI.as_view(),
         name='delivery_info'
    ),
    
    
]
