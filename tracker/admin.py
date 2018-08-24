# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Ticket

# Register your models here.
def make_todo(ModelAdmin,request, queryset):
  queryset.update(status='TODO')
make_todo.short_description = "Mark selected as todo"

def make_doing(ModelAdmin,request, queryset):
  queryset.update(status='DOING')
make_doing.short_description = "Mark selected as doing"

def make_done(ModelAdmin,request, queryset):
  queryset.update(status='DONE')
make_done.short_description = "Mark selected as done"

class Admin_Ticket(admin.ModelAdmin):
  list_display = ['id','type','status','description','user','modified','submitted']
  list_editable = ['status','type']
  date_hierarchy = 'submitted'
  # date_hierarchy= 'modified'
  actions = [make_done,make_doing,make_todo]

admin.site.register(Ticket,Admin_Ticket)