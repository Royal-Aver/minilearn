from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView)

from api.views import (
    RegisterView,
    ProfileView,
    CourseListView,
    CourseDetailView)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs', SpectacularSwaggerView.as_view(
        url_name='schema'), name='swagger-ui'),

    path('api/token/', TokenObtainPairView.as_view(),
            name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
            name='token_refresh'),

    path('api/v1/register/', RegisterView.as_view(), name='register'),
    path('api/v1/profile/', ProfileView.as_view(), name='profile'),

    path('api/v1/courses/', CourseListView.as_view(), name='course-list'),

    path('api/v1/courses/<slug:slug>/', CourseDetailView.as_view(), name='course-detail'),


]
