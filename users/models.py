from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя с дополнительными полями.
    """
    is_teacher = models.BooleanField(
        default=False,
        verbose_name="Преподаватель",
        help_text="Отмечает, может ли пользователь создавать курсы"
    )
    bio = models.TextField(
        blank=True,
        verbose_name="О себе",
        help_text="Короткое описание профиля"
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name="Аватар"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.get_full_name() or self.username
