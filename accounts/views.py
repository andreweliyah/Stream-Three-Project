# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from accounts.forms import UserRegistrationForm, UserLoginForm
from .models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from tracker.models import Ticket, Comment, UpVote
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET
devTrackerPlan = settings.DEV_TRACKER_PLAN
pubKey = settings.STRIPE_PUBLISHABLE

# Create your views here.
# >signup page view
def signup(request):
  if request.user.is_authenticated:
    return redirect(reverse('accounts:profile'))

  form = UserRegistrationForm()
  return render(request, 'accounts/form.html', {'form': form, 'title': 'Create New Account'})

# >login page view
def login(request):
  if request.user.is_authenticated:
    return redirect(reverse('accounts:profile'))

  form = UserLoginForm()
  args = {'form':form}
  args.update(csrf(request))
  args['title'] = 'Login'
  return render(request, 'accounts/form.html', args)

# >profile page view
@login_required(login_url='accounts:login') 
def profile(request):
  user = get_object_or_404(User, id=request.user.id)
  args = {}
  try:
    allTickets = Ticket.objects.all()
    tickets = Ticket.objects.filter(user=user)
    comments = Comment.objects.filter(user=user)
    votes = UpVote.objects.filter(user=user)
    args['alltickets'] = allTickets
    args['tickets'] = tickets
    args['comments'] = comments
    args['votes'] = votes
  except Exception as e:
    print e

  return render(request, 'accounts/profile.html',args)

# >settings pageview
@login_required(login_url='accounts:login')
def settings(request):
  return render(request, 'accounts/settings.html',{"subscription":request.user.subscription,"pubkey":pubKey})

# >settings pageview
def delete(request):
  user = get_object_or_404(User, id=request.user.id)
  if user.stripe_id:
    customer = stripe.Customer.retrieve(user.stripe_id)
    subscription = stripe.Subscription.retrieve(customer.subscriptions.data[0].id)
    subscription.delete()
  user.delete()
      
  return redirect('tracker:index')