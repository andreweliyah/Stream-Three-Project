# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Ticket, Comment, UpVote
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
# >index view
def index(request):
  # return render(request,"tracker/index.html") # This is the original to be restored later
  tickets = Ticket.objects.all()
  page = request.GET.get('page', 1)
  paginator = Paginator(tickets, 10)
  try:
      tix = paginator.page(page)
  except PageNotAnInteger:
      tix = paginator.page(1)
  except EmptyPage:
      tix = paginator.page(paginator.num_pages)

  return render(request,'tracker/index.html',{'tickets':tix})