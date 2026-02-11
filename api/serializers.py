from rest_framework import serializers

from users.models import CustomUser
from courses.models import Course
from lessons.models import Lesson


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'email',
            'is_teacher',
            'bio',
            'avatar',)
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
        validated_data.pop('password1')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_teacher=validated_data.get('is_teacher', False)
        )
        return user


class LessonSerializer(serializers.ModelSerializer):
    """
    Простой сериализатор для уроков.
    Показывает основные поля без тяжёлого контента.
    """
    class Meta:
        model = Lesson
        fields = (
            'id',
            'title',
            'slug',
            'order',
            'content_type',
            'video_url',
            'duration_minutes',
            'is_published'
        )
        read_only_fields = ('id', 'slug', 'order')


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для курсов.
    Показывает основную информацию о курсе + вложенный список уроков.
    """
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'slug',
            'description',
            'teacher',
            'category',
            'created_at',
            'is_published',
            'cover_image',
            'lessons'
        )
        read_only_fields = ('id', 'created_at', 'slug', 'lessons')
