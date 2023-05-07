from django.db import models
from ..users.models import User


class TimeTable(models.Model):
    title = models.CharField(max_length=150)
    contents = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    ## all_date 어떤 의미??

    class Meta:
        abstract = True


class ToDo(TimeTable):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)
    star = models.PositiveSmallIntegerField(default=3)

    class Meta:
        abstract = False


class Schedule(TimeTable):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=50) ## 어떤 목적??
    ## term 어떤 목적??
    ## sort django ORM 이용하면 필요 없음
    ## months 어떤 목적??