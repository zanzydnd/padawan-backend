from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class EmptyBodySerializer(serializers.Serializer):
    pass


class UserCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**validated_data)
        user.password = None
        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'status', 'password')
        read_only_fields = ('id',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')
        read_only_fields = ('id', 'is_active', 'staff', 'admin', 'status', 'email')
