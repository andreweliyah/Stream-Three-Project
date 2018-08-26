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
  if user.stripe_id:
    customer = stripe.Customer.retrieve(user.stripe_id)
    if customer.subscriptions.total_count > 0:
      user.subscription = True
    else:
      user.subscription = False
    user.save()
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

  if user.stripe_id:
    customer = stripe.Customer.retrieve(user.stripe_id)
    if customer.subscriptions.total_count > 0 and customer.subscriptions.data[0].status == 'active':
      args['status'] = True
    else:
      args['status'] = False
    return render(request, 'accounts/profile.html',args)
  else:
    args['status'] = False
    return render(request, 'accounts/profile.html',args)

# >payments
@csrf_exempt
def payments(request):

  user = get_object_or_404(User, id=18)
  if user.stripe_id:
    customer = stripe.Customer.retrieve(user.stripe_id)
    if customer.subscriptions.total_count > 0:
      user.subscription = True
    else:
      subscription = stripe.Subscription.create(
        customer=user.stripe_id,
        items=[{'plan': devTrackerPlan}],
      )
      if customer.subscriptions.total_count > 0:
        user.subscription = True
      else:
        user.subscription = False
  user.save()

  # Refresh profile Page
  return redirect('accounts:profile')

def cancel_subscription(request):
  if request.method == 'POST':
    user = get_object_or_404(User, id=request.user.id)
    customer = stripe.Customer.retrieve(user.stripe_id)
    if customer.subscriptions.total_count == 0:
      request.user.subscription = False
      request.user.save()
    else:
      subscription = stripe.Subscription.retrieve(customer.subscriptions.data[0].id)
      subscription.delete()
      request.user.subscription = False
      request.user.save()
      
  return redirect('accounts:profile')

# >settings pageview
@login_required(login_url='accounts:login')
def settings(request):
  return render(request, 'accounts/settings.html',{"subscription":request.user.subscription})

# >settings pageview
def delete(request):
  user = get_object_or_404(User, id=request.user.id)
  if user.stripe_id:
    customer = stripe.Customer.retrieve(user.stripe_id)
    subscription = stripe.Subscription.retrieve(customer.subscriptions.data[0].id)
    subscription.delete()
  user.delete()
      
  return redirect('tracker:index')