from django.contrib import admin
from .models import Quiz, Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = (
        'text',
        'quiz',
        'order')
    search_fields = ('text',)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'lesson',
        'passing_score')
    search_fields = (
        'title',
        'lesson__title')
