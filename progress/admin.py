from django.contrib import admin
from .models import Enrollment, LessonProgress


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'course',
        'enrolled_at',
        'completed',
        'completed_at')
    list_filter = (
        'completed',
        'course')
    search_fields = (
        'student__username',
        'course__title')
    raw_id_fields = (
        'student',
        'course')


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = (
        'enrollment',
        'lesson',
        'is_completed',
        'progress_percent',
        'completed_at')
    list_filter = (
        'is_completed',
        'enrollment__course')
    search_fields = (
        'enrollment__student__username',
        'lesson__title')
    raw_id_fields = (
        'enrollment',
        'lesson')