# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from accounts.forms import UserRegistrationForm, UserLoginForm
from .models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf

# Create your views here.
# >signup page view
def signup(request):
  if request.user.is_authenticated:
    return redirect(reverse('accounts:profile'))
  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      try:
        user = User.objects.get(email=request.POST.get('email'))
        if user:
          messages.error(request, "This email is already in use. Try logging in instead.")
          return redirect(reverse('accounts:signup'))
      except User.DoesNotExist as e:
        # raise e
        form.save()
        user = auth.authenticate(username=request.POST.get('email'), password=request.POST.get('password1'))
        if user:
          auth.login(request, user)
          messages.success(request, "You have successfully registered")
          return redirect(reverse('accounts:profile'))
        else:
          messages.error(request, 'Sorry there was a problem logging you in. Please try again later.')
  else:
    form = UserRegistrationForm()
  return render(request, 'accounts/signup.html', {'form': form})

# >profile page view
@login_required(login_url='accounts:login')
# >LOGIN PAGE VIEW
def login(request):
  if request.user.is_authenticated:
    return redirect(reverse('accounts:profile'))
  if request.method == 'POST':
    form = UserLoginForm(request.POST)
    if form.is_valid():
      user = auth.authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
      if user is not None:
        auth.login(request, user)
        messages.success(request, 'You are now signed in')
        return redirect(reverse('accounts:profile'))
      else:
        messages.error(request, 'Your email or password is incorrect')
  else:
    form = UserLoginForm()
  args = {'form':form}
  args.update(csrf(request))
  return render(request, 'accounts/login.html', args)
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
    pass

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

# >logout page view
def logout(request):
  auth.logout(request)
  messages.success(request, 'You have successfully logged out')
  return redirect(reverse('accounts:signup'))

# >login page view
def login(request):
  if request.user.is_authenticated:
    return redirect(reverse('accounts:profile'))
  if request.method == 'POST':
    form = UserLoginForm(request.POST)
    if form.is_valid():
      user = auth.authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
      if user is not None:
        auth.login(request, user)
        messages.success(request, 'You are now signed in')
        return redirect(reverse('accounts:profile'))
      else:
        messages.error(request, 'Your email or password is incorrect')
  else:
    form = UserLoginForm()
  args = {'form':form}
  args.update(csrf(request))
  return render(request, 'accounts/login.html', args)
