from django.db import models
from django.utils import timezone
from users.models import CustomUser
from courses.models import Course
from lessons.models import Lesson


class Enrollment(models.Model):
    """
    Запись студента на курс.
    """
    student = models.ForeignKey(
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name="Студент",
        limit_choices_to={'is_teacher': False}
    )
    course = models.ForeignKey(
        to=Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name="Курс"
    )
    enrolled_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата записи"
    )
    completed = models.BooleanField(
        default=False,
        verbose_name="Курс завершён"
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата завершения"
    )

    class Meta:
        verbose_name = "Запись на курс"
        verbose_name_plural = "Записи на курсы"
        unique_together = ['student', 'course']
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.student} → {self.course.title}"

    def mark_as_completed(self):
        if not self.completed:
            self.completed = True
            self.completed_at = timezone.now()
            self.save()

    def progress_percentage(self):
        """Процент прохождения курса студентом"""
        total_lessons = self.course.lessons.count()
        if total_lessons == 0:
            return 0
        completed_lessons = self.lesson_progress.filter(is_completed=True).count()
        return round((completed_lessons / total_lessons) * 100, 1)


class LessonProgress(models.Model):
    """
    Прогресс студента по конкретному уроку.
    """
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='lesson_progress',
        verbose_name="Запись на курс"
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='progress_records',
        verbose_name="Урок"
    )
    is_completed = models.BooleanField(
        default=False,
        verbose_name="Урок пройден"
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата прохождения"
    )
    progress_percent = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Процент прохождения",
        help_text="0–100%"
    )
    last_viewed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Последний просмотр"
    )

    class Meta:
        verbose_name = "Прогресс урока"
        verbose_name_plural = "Прогресс уроков"
        unique_together = ['enrollment', 'lesson']
        ordering = ['lesson__order']

    def __str__(self):
        return f"{self.enrollment} → {self.lesson.title}"

    def complete(self, percent=100):
        if not self.is_completed:
            self.is_completed = True
            self.progress_percent = percent
            self.completed_at = timezone.now()
            self.save()