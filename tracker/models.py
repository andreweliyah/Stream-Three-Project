# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.conf import settings
from tinymce.models import HTMLField
User = settings.AUTH_USER_MODEL

# Create your models here.
# >Ticket
class Ticket(models.Model):
  type = models.CharField(
    max_length=7,
    choices=(
      ('BUG','Bug'),
      ('FEATURE','Feature')
    ),
    default='BUG'
  )
  description = HTMLField()
  status = models.CharField(
    max_length = 5,
    choices = (
      ('TODO','Todo'),
      ('DOING','Doing'),
      ('DONE','Done')
    ),
    default = 'TODO'
  )
  submitted = models.DateField(auto_now_add=True)
  modified = models.DateField(auto_now=True)
  votes = models.IntegerField(default=0)
  user = models.ForeignKey(User,unique=False,blank=True)

  def __unicode__(self):
    return str(self.id)

# >Comment
class Comment(models.Model):
  ticket = models.ForeignKey('Ticket')
  comment = HTMLField()
  user = models.ForeignKey(User,unique=False,blank=True)
  submitted = models.DateField(auto_now_add=True)

# >UpVote
class UpVote(models.Model):
  ticket = models.ForeignKey('Ticket',unique=False)
  user = models.ForeignKey(User,unique=False,blank=True)
