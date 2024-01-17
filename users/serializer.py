from rest_framework import serializers 
from .models import User
from djoser.serializers import UserCreateSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'name'
        ]

class UserCreationSerializer(UserCreateSerializer):
    courses = serializers.ListField(source='')
    class Meta(UserCreateSerializer.Meta):
        model = User 
        fields = ["id","name", "email", "courses"]