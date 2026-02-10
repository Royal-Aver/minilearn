from django.db import models
from django.utils.text import slugify
from courses.models import Course

class Lesson(models.Model):
    """
    Урок внутри курса. Может быть текстом, видео, файлом или квизом.
    """
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name="Курс"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Название урока"
    )
    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
        verbose_name="Slug"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок",
        help_text="Порядковый номер урока в курсе"
    )
    content_type = models.CharField(
        max_length=20,
        choices=[
            ('text', 'Текстовый урок'),
            ('video', 'Видео'),
            ('file', 'Файл/документ'),
            ('quiz', 'Тест/квиз'),
        ],
        default='text',
        verbose_name="Тип контента"
    )
    content = models.TextField(
        blank=True,
        verbose_name="Текст/описание",
        help_text="Основной текст урока или Markdown"
    )
    video_url = models.URLField(
        blank=True,
        verbose_name="Ссылка на видео",
        help_text="YouTube, Vimeo или прямой URL"
    )
    file = models.FileField(
        upload_to='lesson_files/',
        blank=True,
        null=True,
        verbose_name="Прикреплённый файл"
    )
    duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Продолжительность (мин)"
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликован"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['course', 'order']
        unique_together = ['course', 'slug']

    def has_quiz(self):
        return hasattr(self, 'quiz') and self.quiz is not None

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Lesson.objects.filter(slug=slug, course=self.course).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.title} → {self.title}"