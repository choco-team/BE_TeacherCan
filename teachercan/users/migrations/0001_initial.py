# Generated by Django 4.2.4 on 2024-02-12 14:03

from django.conf import settings
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(db_index=True, error_messages={'unique': '이미 해당 이메일로 회원가입 되었습니다.'}, help_text='이메일을 입력해주세요.', max_length=254, unique=True, validators=[django.core.validators.EmailValidator()], verbose_name='email address')),
                ('social_id', models.CharField(blank=True, max_length=50, null=True)),
                ('nickname', models.CharField(db_index=True, help_text='닉네임을 입력해주세요. 문자, 숫자, 특수문자는 @/./+/-/_ 만 가능합니다.', max_length=50, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='nickname')),
                ('gender', models.CharField(choices=[('남', '남'), ('여', '여')], default='남', max_length=2)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('joined_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar_sgv', models.CharField(max_length=50, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Allergy',
            fields=[
                ('code', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'allergy',
            },
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'student_list_column',
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('code', models.CharField(db_index=True, max_length=10, primary_key=True, serialize=False)),
                ('area_code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'school',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('number', models.IntegerField()),
                ('gender', models.CharField(choices=[('남', '남'), ('여', '여')], default='남', max_length=2)),
            ],
            options={
                'db_table': 'student',
            },
        ),
        migrations.CreateModel(
            name='StudentList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('is_main', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('has_allergy', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'student_list',
            },
        ),
        migrations.CreateModel(
            name='StudentAllergyRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allergy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.allergy')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
            options={
                'db_table': 'student_allergy_set',
            },
        ),
        migrations.AddField(
            model_name='student',
            name='allergy',
            field=models.ManyToManyField(through='users.StudentAllergyRelation', to='users.allergy'),
        ),
        migrations.AddField(
            model_name='student',
            name='student_list',
            field=models.ForeignKey(db_column='list_id', on_delete=django.db.models.deletion.CASCADE, to='users.studentlist'),
        ),
        migrations.CreateModel(
            name='Row',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
                ('column', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.column')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
            options={
                'db_table': 'student_list_row',
            },
        ),
        migrations.AddField(
            model_name='column',
            name='student_list',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.studentlist'),
        ),
        migrations.AddField(
            model_name='user',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.school'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
