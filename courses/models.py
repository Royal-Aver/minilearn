from django.db import models
from django.utils.text import slugify
from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название"
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        verbose_name="Slug"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Название курса"
    )
    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
        verbose_name="Slug"
    )
    description = models.TextField(
        verbose_name="Описание"
    )
    teacher = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='taught_courses',
        limit_choices_to={'is_teacher': True},
        verbose_name="Преподаватель"
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses',
        verbose_name="Категория"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Обновлён"
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликован"
    )
    cover_image = models.ImageField(
        upload_to='course_covers/',
        blank=True,
        null=True,
        verbose_name="Обложка"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title