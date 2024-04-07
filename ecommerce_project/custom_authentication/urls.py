#Authentication

from django.urls import path
from .views import MyTokenObtainPairView, RegisterView

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='generate_token'),
    path('register/', RegisterView.as_view(), name='register_user'),
]
