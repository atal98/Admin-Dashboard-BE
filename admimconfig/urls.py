from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/user/', include('user.urls')),
    path('api/order/', include('order.urls')),
    path('api/delivery/', include('delivery.urls')),
    path('api/stats/', include('stats.urls')),
    # path('',TemplateView.as_view(template_name='index.html')),
]
