from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, LessonPlan, PortfolioFolder, PortfolioActivity, UserSettings


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )


@admin.register(LessonPlan)
class LessonPlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'uploaded_at', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'user__username', 'user__email']
    date_hierarchy = 'created_at'


@admin.register(PortfolioFolder)
class PortfolioFolderAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher', 'class_name', 'created_at']
    list_filter = ['created_at', 'class_name']
    search_fields = ['name', 'teacher__username', 'class_name']
    date_hierarchy = 'created_at'


@admin.register(PortfolioActivity)
class PortfolioActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'folder', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description', 'folder__name']
    date_hierarchy = 'created_at'


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'language', 'theme', 'profile_visibility']
    list_filter = ['language', 'theme', 'profile_visibility']
    search_fields = ['user__username', 'user__email']
