# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone

# Create your models here.
class AccountUserManager(UserManager):
  def _create_user(self, username, email, password,
                   is_staff, is_superuser, **extra_fields):
    now = timezone.now()
    if not email:
        raise ValueError('The given username must be set')

    email = self.normalize_email(email)
    user = self.model(username=email, email=email,
                      is_staff=is_staff, is_active=True,
                      is_superuser=is_superuser,
                      date_joined=now, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    
    return user
 
class User(AbstractUser): 
  stripe_id = models.CharField(max_length=40, null=True)
  subscription = models.CharField(max_length=40,null=True)
  STATUS_CHOICES = (
    ('ACTIVE', 'active'),
    ('CANCELED', 'canceled'),
  )
  status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="canceled")
  sub_end = models.IntegerField(null=True)
  # jwt = models.CharField(null=True) # store jwt in database for better access
  objects = AccountUserManager()

