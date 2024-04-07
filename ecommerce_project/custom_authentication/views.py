from .models import CustomUser
from .serializers import MyTokenObtainPairSerializer,RegisterSerializer
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer