from django.db import models

class Column(models.Model):
    field = models.CharField(max_length=20)
    student_list = models.ForeignKey(
        to="student_lists.StudentList", on_delete=models.CASCADE, null=True, related_name='columns'
    )

    class Meta:
        db_table = "student_list_column"