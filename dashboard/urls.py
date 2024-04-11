from django.contrib import admin
from django.urls import path
from dashboard.views import *

urlpatterns = [
    path('total_user/',
         TotalUserAPI.as_view(),
         name='total_user'
    ),
    path('total_order_fulfill/',
         TotalOrderFulfillAPI.as_view(),
         name='total_order_fulfill'
    ),
    path('total_revenue/',
         TotalRevenueAPI.as_view(),
         name='total_revenue'
    ),
    path('total_gross_profit/',
         TotalGrossProfitAPI.as_view(),
         name='total_gross_profit'
    ),
    path('last_six_months_revenue/',
         LastSixMonthsRevenueAPI.as_view(),
         name='last_six_months_revenue'
    ),
    path('target/',
         TargetAPI.as_view(),
         name='target'
    ),
    
]
