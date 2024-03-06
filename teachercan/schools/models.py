from django.db import models


class School(models.Model):
    code = models.CharField(max_length=10, null=False, primary_key=True, db_index=True)
    area_code = models.CharField(max_length=10, null=False)
    name = models.CharField(max_length=10, null=False)

    class Meta:
        db_table = "school"

    def __str__(self):
        return self.name
