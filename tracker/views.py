# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .forms import TicketForm, CommentForm
from .models import Ticket, Comment, UpVote
from django.http import HttpResponse
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core import serializers
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.conf import settings
User = settings.AUTH_USER_MODEL

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
  # Temp - Process form
  if request.method == 'POST':
    form = TicketForm(request.POST)
    if form.is_valid():
      form = form.save(commit=False)
      form.user_id = request.user.id  
      # form.submitted = timezone.now
      # form.modified = ''
      form.save()
      # return render(request,'tracker/index.html',{'form':form})
      return redirect('tracker:index')
  else:
    # Temp - Display form
    form = TicketForm()
  return render(request,'tracker/form.html',{'form':form}) 

# >ticket view
def ticket(request, id):
  ticket = get_object_or_404(Ticket, id=id) # The specific ticketdetail
  comments = Comment.objects.filter(ticket=ticket) # All comments for this (ticket variable) specific ticketdetail

  if request.method == 'POST':
    form = CommentForm(request.POST) # The populated form for the new comment
    if form.is_valid():
      comment = form.save(commit=False) # Assign form to comment variable without saving to data base. I need to change something first.
      comment.ticket = ticket # Added the current ticket to the comment's foreign key 'ticket'.
      comment.user_id = request.user.id # User Id
      comment.save() # Save changes
      form = CommentForm() # reset form for new comments
      # Return template
      return render(request, 'tracker/ticketdetail.html', {'ticket': ticket,
                                                    'comments': comments,
                                                    'form': form })
  else:
    form = CommentForm()
  return render(request, 'tracker/ticketdetail.html', {'ticket': ticket,
                                                'comments': comments,
                                                'form': form })