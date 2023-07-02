from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, School


class BaseUserAdmin(UserAdmin):
    model = User
    list_display = ("id", "user_id", "is_superuser", "joined_at", "last_login")
    list_filter = ("is_superuser",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "user_id",
                )
            },
        ),
        (
            "Personal info",
            {
                "fields": (
                    "nickname",
                    "email",
                    "social_id",
                    "is_male",
                    "birthday",
                )
            },
        ),
        ("School info", {"fields": ("school_code",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Important dates",
            {
                "fields": (
                    "last_login",
                    "joined_at",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "user_id",
                    "password1",
                    "password2",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("user_id", "email")
    ordering = ("id",)
    readonly_fields = ("id",)


admin.site.register(User, BaseUserAdmin)
admin.site.register(School)
