# Generated by Django 4.2.4 on 2024-02-25 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentlist',
            name='description',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
