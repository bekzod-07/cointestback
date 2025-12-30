from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Qo‘shimcha", {"fields": ("grade",)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Qo‘shimcha", {"fields": ("grade",)}),
    )

    list_display = ("username", "grade", "is_staff", "is_active")
    list_filter = ("grade", "is_staff", "is_active")
