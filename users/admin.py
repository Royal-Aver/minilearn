from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


# admin.site.register(CustomUser)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'is_teacher',
        'is_staff',
        'date_joined')
    list_filter = (
        'is_teacher',
        'is_staff',
        'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('is_teacher', 'bio', 'avatar')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительно', {'fields': ('is_teacher',)}),
    )
