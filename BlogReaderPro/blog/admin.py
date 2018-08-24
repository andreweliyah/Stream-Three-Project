# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Post

class Admin_Post(admin.ModelAdmin):
  list_display = ['title','author','created_date','published_date','tag','image']
  list_editable = [
    'tag',
    'author',
    # 'image'
  ]

admin.site.register(Post, Admin_Post)
