# Generated by Django 4.2.2 on 2023-07-02 07:21

import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_school_remove_user_area_code_remove_user_school_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='school',
            old_name='school_code',
            new_name='code',
        ),
        migrations.RenameField(
            model_name='school',
            old_name='school_name',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, error_messages={'unique': '이미 해당 이메일로 회원가입 되었습니다.'}, help_text='이메일을 입력해주세요.', max_length=254, null=True, unique=True, validators=[django.core.validators.EmailValidator()], verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(blank=True, help_text='닉네임을 입력해주세요. 문자, 숫자, 특수문자는 @/./+/-/_ 만 가능합니다.', max_length=50, null=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='nickname'),
        ),
        migrations.AlterField(
            model_name='user',
            name='school_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.school'),
        ),
        migrations.AlterField(
            model_name='user',
            name='social_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
