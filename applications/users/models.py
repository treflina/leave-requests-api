import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(
        verbose_name=_("username"), max_length=30, db_index=True, unique=True
    )
    first_name = models.CharField(verbose_name=_("first name"), max_length=50)
    last_name = models.CharField(verbose_name=_("last name"), max_length=50)
    additional_identifier = models.CharField(
        _("additional_identifier"),
        max_length=50,
        blank=True,
        null=True,
        help_text=_(
            """can be used eg. to differentiate employees with the same name or
        a person working on more than one position"""
        ),
    )
    email = models.EmailField("email", null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return f"{self.first_name.title()} {self.last_name.title()} \
{self.additional_identifier}"

    @property
    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    @property
    def get_unique_name(self):
        return f"{self.first_name.title()} {self.last_name.title()} \
{self.additional_identifier}"
