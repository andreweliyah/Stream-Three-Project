# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Ticket, Comment, UpVote
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import TicketForm,

# Create your views here.
# >index view
def index(request):
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

# >form view
@login_required(login_url='accounts:login')
def form(request): 
  if request.method == 'POST':
    form = TicketForm(request.POST)
    if form.is_valid():
      form = form.save(commit=False)
      form.user_id = request.user.id  
      form.save()
      return redirect('tracker:index')
  else:
    form = TicketForm()
  return render(request,'tracker/form.html',{'form':form}) 