from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin)
import os
import jwt


class UserManager(BaseUserManager):
    def create_user(self, username, email, phone, bio='', image='', password=None):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            phone=phone,
            bio=bio,
            image=image,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        if not password:
            password = None

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username=username, email=email, password=password)
        user.is_superuser = True
        user.is_staff = True

        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, unique=True, max_length=255)
    email = models.EmailField(db_index=True, unique=True, max_length=255)
    phone = models.CharField(unique=True, max_length=20, default='000000000000')
    bio = models.CharField(max_length=255)
    image = models.URLField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
