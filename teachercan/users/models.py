from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core.validators import EmailValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail


class BaseUser(AbstractBaseUser, PermissionsMixin):

    email_validator = EmailValidator()
    nickname_validator = UnicodeUsernameValidator()

    email = models.EmailField(
        _("email address"),
        unique=True,
        help_text=_(
            "이메일을 입력해주세요."
        ),
        validators=[email_validator],
        error_messages={
            "unique": _("이미 해당 이메일로 회원가입 되었습니다."),
        },
    )
    username = models.CharField(
        _("nickname"),
        max_length=50,
        unique=True,
        help_text=_(
            "닉네임을 입력해주세요. 문자, 숫자, 특수문자는 @/./+/-/_ 만 가능합니다."
        ),
        validators=[nickname_validator],
        error_messages={
            "unique": _("해당 닉네임은 다른 사람이 사용중입니다."),
        },
    )
    realname = models.CharField(_("realname"), max_length=150, blank=True)
    
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
