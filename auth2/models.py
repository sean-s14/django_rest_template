from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings
from .utils import code_generator, name_generator

USER = settings.AUTH_USER_MODEL


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length  = 150,
        unique      = True,
        help_text   = _("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators  = [username_validator],
        error_messages = {"unique": _("A user with that username already exists."),},
        default=name_generator
    )
    is_verified = models.BooleanField(blank=True, null=True, default=False)
    code        = models.CharField(max_length=6, blank=True, null=True, default=code_generator)
    imageURI    = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username