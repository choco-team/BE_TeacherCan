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
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail


class School(models.Model):
    code = models.CharField(max_length=10, null=False, primary_key=True, db_index=True)
    area_code = models.CharField(max_length=10, null=False)
    name = models.CharField(max_length=10, null=False)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("email를 입력해주세요.")
        user = self.model(email=email, **extra_fields)
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
        help_text=_("닉네임을 입력해주세요. 문자, 숫자, 특수문자는 @/./+/-/_ 만 가능합니다."),
        validators=[nickname_validator],
    )
    school = models.ForeignKey(School, null=True, blank=True, on_delete=models.SET_NULL)
    is_male = models.BooleanField(null=True)
    birthday = models.DateField(null=True, blank=True)
    joined_at = models.DateTimeField(_("date joined"), default=timezone.now)
    avatar_sgv = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
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
    description = models.TextField(null=True, blank=True)
    has_allergy = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Allergy(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)


class Student(models.Model):
    name = models.CharField(max_length=10)
    number = models.IntegerField()
    is_male = models.BooleanField()
    description = models.TextField(null=True, blank=True)

    student_list = models.ForeignKey(
        StudentList, on_delete=models.CASCADE, db_column="list_id"
    )
    allergy = models.ManyToManyField(Allergy, db_column="allergy_code")


class Column(models.Model):
    field = models.CharField(max_length=20)
    value = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    student = models.ForeignKey(to="Student", on_delete=models.CASCADE, null=True)
    student_list = models.ForeignKey(
        to="StudentList", on_delete=models.CASCADE, null=True
    )


# class User(AbstractBaseUser, PermissionsMixin):
#     email_validator = EmailValidator()
#     nickname_validator = UnicodeUsernameValidator()

#     email = models.EmailField(
#         _("email address"),
#         unique=True,
#         help_text=_(
#             "이메일을 입력해주세요."
#         ),
#         validators=[email_validator],
#         error_messages={
#             "unique": _("이미 해당 이메일로 회원가입 되었습니다."),
#         },
#     )
#     username = models.CharField(
#         _("nickname"),
#         max_length=50,
#         unique=True,
#         help_text=_(
#             "닉네임을 입력해주세요. 문자, 숫자, 특수문자는 @/./+/-/_ 만 가능합니다."
#         ),
#         validators=[nickname_validator],
#         error_messages={
#             "unique": _("해당 닉네임은 다른 사람이 사용중입니다."),
#         },
#     )
#     realname = models.CharField(_("realname"), max_length=150, blank=True)

#     is_certificated = models.BooleanField(
#         _("certifacation"),
#         default=False,
#         help_text=_("Designates whether the user has been certificated"),
#     )
#     is_staff = models.BooleanField(
#         _("staff status"),
#         default=False,
#         help_text=_("Designates whether the user can log into this admin site."),
#     )
#     is_active = models.BooleanField(
#         _("active"),
#         default=True,
#         help_text=_(
#             "Designates whether this user should be treated as active. "
#             "Unselect this instead of deleting accounts."
#         ),
#     )
#     date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

#     objects = UserManager()

#     EMAIL_FIELD = "email"
#     USERNAME_FIELD = "username"
#     REQUIRED_FIELDS = ["email"]

#     def __str__(self):
#         return self.username

#     def clean(self):
#         super().clean()
#         self.email = self.__class__.objects.normalize_email(self.email)

#     def email_user(self, subject, message, from_email=None, **kwargs):
#         """Send an email to this user."""
#         send_mail(subject, message, from_email, [self.email], **kwargs)


# class School(models.Model):
#     name = models.CharField(max_length=100, blank=True, null=True)
#     code = models.PositiveIntegerField()
#     area = models.PositiveIntegerField()
#     address = models.CharField(max_length=150, blank=True, null=True)


# #TODO Django Taggit 활용
# # class Tag(models.Model):
# #     name = models.CharField(max_length=100, blank=True, null=True)


# class News(models.Model):
#     keyword = models.CharField(max_length=100)


# ## Link / HomeLink 합쳐도 괜찮음??
# class Link(models.Model):
#     title = models.CharField(max_length=100)
#     memo = models.TimeField(blank=True, null=True)
#     url = models.URLField(blank=True, null=True) ## 추가 : 추후 사용자가 생성도 가능??
#     is_home = models.BooleanField(default=False)


# class DDay(models.Model):
#     title = models.CharField(max_length=100)
#     date = models.DateField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)


# class UserDetail(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     bg_theme = models.PositiveIntegerField()
#     ## allergy : students 앱에 생성
#     #TODO tag : 추후 django taggit 적용
#     news = models.ManyToManyField(News)
#     links = models.ManyToManyField(Link)
#     agree_policy = models.BooleanField(default=False)
#     ## dday : DDay 모델 별도 생성
#     is_move_dday = models.BooleanField(default=False) ## 어떤 목적??
#     # home_links = models.ManyToManyField(Link)
#     default_student_list_id = models.CharField(max_length=50, null=True) ## 어떤 목적??


# ##TimeRecord를 전부 다 저장하는 것이 좋을까 / 가장 마지막 로그인만 저장하는 것이 좋을까?
