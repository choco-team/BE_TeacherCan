# Generated by Django 4.2 on 2023-06-25 14:22

import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': '이미 해당 이메일로 회원가입 되었습니다.'}, help_text='이메일을 입력해주세요.', max_length=254, null=True, unique=True, validators=[django.core.validators.EmailValidator()], verbose_name='email_address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(help_text='닉네임을 입력해주세요. 문자, 숫자, 특수문자는 @/./+/-/_ 만 가능합니다.', max_length=50, null=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='nickname'),
        ),
        migrations.AlterField(
            model_name='user',
            name='social_id',
            field=models.CharField(max_length=50, null=True),
        ),
    ]