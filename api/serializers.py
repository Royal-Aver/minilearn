from rest_framework import serializers
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'email',
            'is_teacher',
            'bio',
            'avanar',)
        read_only_fields = ('id',)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password1 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "password",
            "password1",
            "is_teacher")

        def validate(self, attrs):
            if attrs['password'] != attrs['password1']:
                raise serializers.ValidationError(
                    {"password": "Пароли не совпадают"})
            return attrs

        def create(self, validated_data):
            user = CustomUser.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                is_teacher=validated_data.get('is_teacher', False)
            )
            return user