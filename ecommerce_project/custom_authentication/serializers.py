from .models import CustomUser
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email

        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=CustomUser.objects.all())])

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')

    def create(self, validated_data) -> CustomUser:
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user