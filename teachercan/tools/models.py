from django.db import models
from django.utils.translation import gettext_lazy as _


class Color(models.TextChoices):
    ORANGE = "orange", _("주황")
    RED = "red", _("빨강")
    PURPLE = "purple", _("보라")
    #TODO 더 작성 필요!
