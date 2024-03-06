from django.contrib import admin

from .models import School
from ..users.models import User


class UserInline(admin.TabularInline):
    model = User
    extra = 1


class SchoolInline(admin.TabularInline):
    model = School


class SchoolAdmin(admin.ModelAdmin):
    fieldsets = [
        ("None", {"fields": ["code", "area_code", "name"]}),
    ]
    search_fields = ("name",)
    inlines = [UserInline]


admin.site.register(School, SchoolAdmin)
