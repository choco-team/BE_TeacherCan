# Generated by Django 4.2.4 on 2023-08-09 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='code',
            field=models.CharField(db_index=True, max_length=10, primary_key=True, serialize=False),
        ),
    ]