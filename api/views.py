from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer, UserSerializer, CourseSerializer
from users.models import CustomUser
from courses.models import Course


class RegisterView(generics.CreateAPIView):
    """
    Эндпоинт для регистрации нового пользователя.
    Принимает username, email, password, password2, is_teacher (опционально).
    Возвращает данные нового пользователя без пароля.
    """
    queryset = CustomUser.objects.all()
    permission_classes = []  # открыто для всех
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user).data,
            "message": "Пользователь успешно зарегистрирован"
        }, status=status.HTTP_201_CREATED)


class ProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class CourseListView(generic.ListAPIview):
    """
    Список всех курсов.
    Пока доступен всем (без авторизации).
    """
    courses = Course.objects.all()
    serializer_class = CourseSerializer