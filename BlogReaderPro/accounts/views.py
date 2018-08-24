# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from accounts.forms import UserRegistrationForm
from .models import User
from django.contrib import auth,messages

# Create your views here.
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