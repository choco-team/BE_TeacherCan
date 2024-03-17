from django.db import models


class StudentList(models.Model):
    name = models.CharField(max_length=15)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    has_allergy = models.BooleanField(default=False)
    description = models.CharField(null=True, max_length=200)

    user = models.ForeignKey(to="users.User", on_delete=models.CASCADE)

    class Meta:
        db_table = "student_list"
