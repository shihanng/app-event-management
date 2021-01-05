from typing import List

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = []

    def has_perms(self, perm, obj=None):  # pylint: disable=R0201,W0613
        return True

    def has_module_perms(self, app_label):  # pylint: disable=R0201,W0613
        return True

    def is_staff(self):  # pylint: disable=R0201
        return True

    def is_active(self):  # pylint: disable=R0201
        return True
