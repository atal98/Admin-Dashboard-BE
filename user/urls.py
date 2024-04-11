from django.contrib import admin
from django.urls import path
from user.views import *

urlpatterns = [
    path('user_table/',
         UserTableAPI.as_view(),
         name='user_table'
    ),
    path('single_user/<int:pk>/',
         UserSinigleAPI.as_view(),
         name='single_user'
    ),
    path('total_retention_rate/',
         TotalRetentionRateAPI.as_view(),
         name='total_retention_rate'
    ),
    path('total_churn_rate/',
         TotalChurnRateAPI.as_view(),
         name='total_churn_rate'
    ),
    path('total_conversion_rate/',
         TotalConversionRateAPI.as_view(),
         name='total_conversion_rate'
    ),
    
]
