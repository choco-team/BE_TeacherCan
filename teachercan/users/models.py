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
from django.utils.translation import gettext_lazy as _


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
        to="schools.School", null=True, blank=True, on_delete=models.SET_NULL
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
