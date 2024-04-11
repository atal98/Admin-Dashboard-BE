from django.contrib import admin
from django.urls import path
from order.views import *

urlpatterns = [
    path('total_order/',
         TotalOrderAPI.as_view(),
         name='total_order'
    ),
    path('total_order_value/',
         TotalOrderValueAPI.as_view(),
         name='total_order_value'
    ),
    path('total_avg_order_value/',
         TotalAvgOrderValueAPI.as_view(),
         name='total_avg_order_value'
    ),
    path('total_order_return/',
         TotalOrderReturnRateAPI.as_view(),
         name='total_order_return'
    ),
    path('last_six_months_order_fulfill/',
         LastSixMonthsOrdersFulFillAPI.as_view(),
         name='last_six_months_order_fulfill'
    ),
    path('order_status_distribution/',
         OrderStatusDistributionAPI.as_view(),
         name='order_status_distribution'
    ),
]
