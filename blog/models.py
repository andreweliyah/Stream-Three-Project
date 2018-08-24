# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.conf import settings
# from settings import AUTH_USER_MODEL as User
from tinymce.models import HTMLField

User = settings.AUTH_USER_MODEL

class Post(models.Model):
  author = models.ForeignKey(User,blank=True)
  title = models.CharField(max_length=200)
  content = HTMLField()
  created_date = models.DateTimeField(auto_now_add=True)
  published_date = models.DateTimeField(blank=True, null=True)
  views = models.IntegerField(default=0)
  tag = models.CharField(max_length=30, blank=True, null=True)
  image = models.ImageField(upload_to="images", blank=True, null=True)

  # def snippet(self):
  #   return self.content[:50] + '...'

  def publish(self):
    self.published_date = timezone.now()
    self.save()

  def __unicode__(self):
    return self.title
