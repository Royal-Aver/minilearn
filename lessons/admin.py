from django.contrib import admin
from .models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'course',
        'order',
        'content_type',
        'is_published')
    list_filter = (
        'course',
        'content_type',
        'is_published')
    search_fields = (
        'title',
        'content')
    prepopulated_fields = {
        'slug': ('title',)
        }
    list_editable = (
        'order',
        'is_published')
