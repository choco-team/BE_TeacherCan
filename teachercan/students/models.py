from django.db import models
from django.utils.translation import gettext_lazy as _
from ..users.models import User


class Allergy(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Role(models.Model):
    title = models.CharField(max_length=50)
    roles = models.CharField(max_length=100) ## 꼭 필요한거?
    detail = models.TextField()

## StudentList 필요 없는거 맞을지??

class Student(models.Model):
    class Gender(models.TextChoices):
        MALE = "남", _("남자")
        FEMALE = "여", _("여자")

    teacher = models.ForeignKey(User, on_delete=models.CASCADE) # teacherEmail
    name = models.CharField(max_length=30)
    number = models.PositiveIntegerField()
    gender = models.CharField(
        choices=Gender.choices
    )
    allergy = models.ManyToManyField(Allergy)
    #TODO tag 필드 추후 구현
    ## listId 어떤 필드?
    is_deleted = models.BooleanField(default=False) # trash 이름 변경
    memo = models.TextField(blank=True, null=True)
    icon = models.PositiveIntegerField() ## 어떤 역할??


class RoleHistory(models.Model):
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
