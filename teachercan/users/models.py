from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.core.validators import EmailValidator
from django.contrib.auth.validators import (
    ASCIIUsernameValidator,
    UnicodeUsernameValidator,
)
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail


class School(models.Model):
    code = models.CharField(max_length=10, null=False, primary_key=True, db_index=True)
    area_code = models.CharField(max_length=10, null=False)
    name = models.CharField(max_length=10, null=False)

    class Meta:
        db_table = "school"

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("email를 입력해주세요.")
        user = self.model(email=email, **extra_fields)
        try:
            validate_password(password)
        except:
            raise ValueError("비밀번호 유효성 검사 실패")
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("is_superuser=True일 필요가 있습니다.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email_validator = EmailValidator()
    nickname_validator = UnicodeUsernameValidator()
    user_id_validator = ASCIIUsernameValidator()

    email = models.EmailField(
        _("email address"),
        db_index=True,
        unique=True,
        null=False,
        help_text=_("이메일을 입력해주세요."),
        validators=[email_validator],
        error_messages={
            "unique": _("이미 해당 이메일로 회원가입 되었습니다."),
        },
    )
    social_id = models.CharField(max_length=50, null=True, blank=True)
    nickname = models.CharField(
        _("nickname"),
        db_index=True,
        max_length=50,
        null=False,
        help_text=_(
            "닉네임을 입력해주세요. 문자, 숫자, 특수문자는 @/./+/-/_ 만 가능합니다."
        ),
        validators=[nickname_validator],
    )
    school = models.ForeignKey(
        to="School", null=True, blank=True, on_delete=models.SET_NULL
    )
    gender = models.CharField(
        null=True, max_length=2, choices=[("남", "남"), ("여", "여")], default="남"
    )
    birthday = models.DateField(null=True, blank=True)
    joined_at = models.DateTimeField(_("date joined"), auto_now_add=True)
    avatar_sgv = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "user"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @property
    def is_staff(self):
        return self.is_superuser


class StudentList(models.Model):
    name = models.CharField(max_length=15)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    has_allergy = models.BooleanField(default=False)
    description = models.CharField(null=True, max_length=200)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "student_list"


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
        StudentList, on_delete=models.CASCADE, db_column="list_id"
    )
    allergy = models.ManyToManyField(to="Allergy", through="StudentAllergyRelation")

    class Meta:
        db_table = "student"


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
