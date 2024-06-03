from django.urls import path
from auth.views import LogoutView, CreateUserView

urlpatterns = [
    path('user/register/', 
         CreateUserView.as_view(),
         name="register"
    ),
    path('logout/', 
         LogoutView.as_view(), 
         name='logout'
    ),
]
