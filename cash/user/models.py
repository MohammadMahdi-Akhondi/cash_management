from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from cash.common.models import BaseModel

class UserManager(BUM):
    def create_user(self, username, is_active=True, is_staff=False, password=None):

        user = self.model(username=username, is_active=is_active, is_staff=is_staff)
        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            is_active=True,
            is_staff=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=255,
        unique=True,
        validators=[username_validator],
        verbose_name=_('username')
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('active')
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('staff status')
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self) -> str:
        return self.username
