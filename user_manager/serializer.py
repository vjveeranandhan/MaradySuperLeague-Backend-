from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.models import User
from urllib.parse import urljoin
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'date_of_birth', 'phone', 'age']

class UserRetrieveSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_of_birth', 'phone', 'age', 'image']
    
    def get_image(self, obj):
        if obj.image:
            return urljoin(settings.BASE_URL, obj.image.url)
        return None

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ['id', 'image']