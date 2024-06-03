from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', 
         TokenObtainPairView.as_view(),
         name="get_token"
    ),
    path('api/token/refresh/', 
         TokenRefreshView.as_view(),
         name="refresh"
    ),
    path('api-auth/', 
         include('rest_framework.urls')
    ),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/user/', include('user.urls')),
    path('api/order/', include('order.urls')),
    path('api/delivery/', include('delivery.urls')),
    path('api/stats/', include('stats.urls')),
    path('api/auth/', include('auth.urls')),
    # path('',TemplateView.as_view(template_name='index.html')),
]
