from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
    School,
    StudentList,
    Student,
    Allergy,
    Column,
    Row,
    StudentAllergyRelation,
)


class SchoolInline(admin.TabularInline):
    model = School


class UserInline(admin.TabularInline):
    model = User
    extra = 1


class SchoolAdmin(admin.ModelAdmin):
    fieldsets = [
        ("None", {"fields": ["code", "area_code", "name"]}),
    ]
    search_fields = ("name",)
    inlines = [UserInline]


class BaseUserAdmin(UserAdmin):
    model = User
    list_display = (
        "id",
        "email",
        "nickname",
        "is_superuser",
        "joined_at",
        "last_login",
        "school",
    )
    list_filter = ("is_superuser",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "email",
                )
            },
        ),
        (
            "Personal info",
            {
                "fields": (
                    "nickname",
                    "social_id",
                    "is_male",
                    "birthday",
                )
            },
        ),
        (
            "School info",
            {"fields": ("school",)},
        ),
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
                    "email",
                    "nickname",
                    "password1",
                    "password2",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "school",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("id",)
    readonly_fields = ("id",)


class StudentAllergyInline(admin.TabularInline):
    model = Student.allergy.through
    extra = 1


class StudentAdmin(admin.ModelAdmin):
    inlines = (StudentAllergyInline,)


admin.site.register(User, BaseUserAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(StudentList)
admin.site.register(Student, StudentAdmin)
admin.site.register(Allergy)
admin.site.register(Column)
admin.site.register(Row)
admin.site.register(StudentAllergyRelation)
