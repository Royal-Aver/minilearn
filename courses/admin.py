from django.contrib import admin

from .models import Course, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'teacher',
        'category',
        'is_published',
        'created_at')
    list_filter = (
        'is_published',
        'category',
        'teacher')
    search_fields = (
        'title',
        'description')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('teacher',)
