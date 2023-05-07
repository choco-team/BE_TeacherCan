from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core.validators import EmailValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail


class User(AbstractBaseUser, PermissionsMixin):
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
    
    is_certificated = models.BooleanField(
        _("certifacation"),
        default=False,
        help_text=_("Designates whether the user has been certificated"),
    )  
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


class School(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    code = models.PositiveIntegerField()
    area = models.PositiveIntegerField()
    address = models.CharField(max_length=150, blank=True, null=True)


#TODO Django Taggit 활용 
# class Tag(models.Model):
#     name = models.CharField(max_length=100, blank=True, null=True)


class News(models.Model):
    keyword = models.CharField(max_length=100)


## Link / HomeLink 합쳐도 괜찮음??
class Link(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TimeField(blank=True, null=True)
    url = models.URLField(blank=True, null=True) ## 추가 : 추후 사용자가 생성도 가능??
    is_home = models.BooleanField(default=False)


class DDay(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bg_theme = models.PositiveIntegerField()
    ## allergy : students 앱에 생성
    #TODO tag : 추후 django taggit 적용
    news = models.ManyToManyField(News)
    links = models.ManyToManyField(Link)
    agree_policy = models.BooleanField()
    ## dday : DDay 모델 별도 생성
    is_move_dday = models.BooleanField() ## 어떤 목적??
    home_links = models.ManyToManyField(Link)
    default_student_list_id = models.CharField() ## 어떤 목적??


##TimeRecord를 전부 다 저장하는 것이 좋을까 / 가장 마지막 로그인만 저장하는 것이 좋을까?
