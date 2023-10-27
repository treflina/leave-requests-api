from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(
        self, first_name, last_name, username, password, **extra_fields
    ):
        if not username:
            raise ValueError(_("Users must have a username."))
        if not first_name:
            raise ValueError(_("Users must have a first name."))
        if not last_name:
            raise ValueError(_("Users must have a last name."))
        if not password:
            raise ValueError(_("Superuser must have a password."))

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            **extra_fields,
        )
        user.set_password(password)

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user.save(using=self._db)
        return user

    def create_superuser(
        self, first_name, last_name, username, password, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        user = self.create_user(
            first_name, last_name, username, password, **extra_fields
        )
        user.save(using=self._db)
        return user
