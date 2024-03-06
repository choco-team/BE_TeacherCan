from django.db import models


class Allergy(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        db_table = "allergy"


class StudentAllergyRelation(models.Model):
    student = models.ForeignKey(to="Student", on_delete=models.CASCADE)
    allergy = models.ForeignKey(to="Allergy", on_delete=models.CASCADE)

    class Meta:
        db_table = "student_allergy_set"


class Student(models.Model):
    name = models.CharField(max_length=10)
    number = models.IntegerField()
    gender = models.CharField(
        max_length=2, choices=[("남", "남"), ("여", "여")], default="남"
    )

    student_list = models.ForeignKey(
        to="StudentList", on_delete=models.CASCADE, db_column="list_id"
    )
    allergy = models.ManyToManyField(to="Allergy", through="StudentAllergyRelation")

    class Meta:
        db_table = "student"


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


class Column(models.Model):
    field = models.CharField(max_length=20)
    student_list = models.ForeignKey(
        to="StudentList", on_delete=models.CASCADE, null=True
    )

    class Meta:
        db_table = "student_list_column"


class Row(models.Model):
    value = models.CharField(max_length=100)
    column = models.ForeignKey(to="Column", on_delete=models.CASCADE)
    student = models.ForeignKey(to="Student", on_delete=models.CASCADE)

    class Meta:
        db_table = "student_list_row"
