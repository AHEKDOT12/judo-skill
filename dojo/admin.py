from django.contrib import admin

from .models import (
    Achievement,
    Group,
    PointEvent,
    Profile,
    Student,
    StudentAchievement,
)
from .services import recalculate_student_points


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'coach', 'created_at')
    list_filter = ('coach',)
    search_fields = ('name', 'coach__username')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'last_name',
        'first_name',
        'age',
        'group',
        'total_points',
        'belt',
        'created_at',
    )
    list_filter = ('group', 'belt')
    search_fields = ('first_name', 'last_name', 'user__username')


@admin.register(PointEvent)
class PointEventAdmin(admin.ModelAdmin):
    list_display = ('student', 'coach', 'points', 'comment', 'created_at')
    list_filter = ('coach', 'created_at')
    search_fields = ('student__first_name', 'student__last_name', 'comment')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        recalculate_student_points(obj.student)

    def delete_model(self, request, obj):
        student = obj.student
        super().delete_model(request, obj)
        recalculate_student_points(student)

    def delete_queryset(self, request, queryset):
        students = list({event.student for event in queryset})
        super().delete_queryset(request, queryset)

        for student in students:
            recalculate_student_points(student)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'icon')
    search_fields = ('title',)


@admin.register(StudentAchievement)
class StudentAchievementAdmin(admin.ModelAdmin):
    list_display = ('student', 'achievement', 'awarded_by', 'awarded_at')
    list_filter = ('achievement', 'awarded_at')
    search_fields = (
        'student__first_name',
        'student__last_name',
        'achievement__title',
    )