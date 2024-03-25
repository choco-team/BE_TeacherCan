from django.contrib import admin

from .models import Student, StudentAllergyRelation, Allergy, Row


class StudentAllergyInline(admin.TabularInline):
    model = Student.allergy.through
    extra = 1


class StudentAdmin(admin.ModelAdmin):
    inlines = (StudentAllergyInline,)


admin.site.register(Student, StudentAdmin)
admin.site.register(Allergy)
admin.site.register(Row)
admin.site.register(StudentAllergyRelation)
