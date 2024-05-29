from django.contrib import admin
from django.urls import path
from stats.views import *

urlpatterns = [
    path('cac/',
         CACAPI.as_view(),
         name='cac'
    ),
    path('sales_vs_customer_vs_lead/',
         SalesExpenseVSCustomerAcqVSTotalLeadsAPI.as_view(),
         name='sales_vs_customer_vs_lead'
    ),
    path('sales_breakdown/',
         SalesExpenseBreakDownAPI.as_view(),
         name='sales_breakdown'
    ),
    path('net_profit_breakdown/',
         NetProfitBreakdownAPI.as_view(),
         name='net_profit_breakdown'
    ),
    path('growth_rate/',
         GrowthRateAPI.as_view(),
         name='growth_rate'
    ),
]