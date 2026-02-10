from django.db import models
from lessons.models import Lesson


class Quiz(models.Model):
    """
    Тест, привязанный к уроку (один урок — один квиз).
    """
    lesson = models.OneToOneField(
        to=Lesson,
        on_delete=models.CASCADE,
        related_name='quiz',
        verbose_name="Урок"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Название теста"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание"
    )
    passing_score = models.PositiveSmallIntegerField(
        default=70,
        verbose_name="Проходной балл (%)"
    )

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    def get_correct_answers_count(self):
        return self.questions.annotate(
            correct_count=models.Count(
                'answers', filter=models.Q(
                    answers__is_correct=True))
        ).aggregate(
            total=models.Sum('correct_count'))['total'] or 0

    def __str__(self):
        return f"Quiz: {self.title} ({self.lesson.title})"


class Question(models.Model):
    quiz = models.ForeignKey(
        to=Quiz,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name="Тест"
    )
    text = models.TextField(
        verbose_name="Текст вопроса"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок"
    )

    class Meta:
        ordering = ['order']
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.text[:50]


class Answer(models.Model):
    question = models.ForeignKey(
        to=Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name="Вопрос"
    )
    text = models.CharField(
        max_length=300,
        verbose_name="Вариант ответа"
    )
    is_correct = models.BooleanField(
        default=False,
        verbose_name="Правильный"
    )

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"

    def __str__(self):
        return self.text[:50]