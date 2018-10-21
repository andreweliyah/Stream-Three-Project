# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..models import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserModelSerializer
from django.http import Http404
import stripe
from ..forms import UserRegistrationForm, UserLoginForm
from django.db import IntegrityError
from django.conf import settings
from django.contrib import auth
from datetime import datetime
from pprint import pprint

stripe.api_key = settings.STRIPE_SECRET
devTrackerPlan = settings.DEV_TRACKER_PLAN

def subscribe(request):
  subscription = stripe.Subscription.create(
    customer=request.user.stripe_id,
    items=[{'plan': devTrackerPlan}],
  )
  return subscription

def createCustomer(request):
  customer = stripe.Customer.create(
    source=request.POST['stripeToken'],
    email=request.user.email,
  )
  return customer

# >user auth managment
class UserAuthAPIView(APIView):
  permission_classes = ()
  def post(self, request):
    try:
      # >>Signup
      form = UserRegistrationForm(request.POST)
      if form.is_valid():
        form.save()
        user = auth.authenticate(username=request.POST.get('email'), password=request.POST.get('password1'))
        if user:
          auth.login(request, user)
      else:
        # >>login
        form = UserLoginForm(request.POST)

        if form.is_valid():
          user = get_object_or_404(User,username=request.POST.get('email'))
          user.is_active = True
          user = auth.authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
          if user is not None:
            auth.login(request, user)
          else:
            return Response({'detail':'invalid email and/or password'}, status=status.HTTP_400_BAD_REQUEST)
        else:
          # >>logout
          if request.user.is_authenticated():
              auth.logout(request)
          else:
            return Response({'detail':'invalid form data'},status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError:
      return Response({'detail':'user exists'},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
      print e
      return Response({'detail':'Error. Please check your login information.'},status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_202_ACCEPTED)

  def delete(self, request):
    # >>delete user and subs
    user = request.user
    if user.is_authenticated():
      try:
        if user.stripe_id:
          customer = stripe.Customer.retrieve(user.stripe_id)
          subscription = stripe.Subscription.retrieve(customer.subscriptions.data[0].id)
          subscription.delete()
      except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
        body = e.json_body
        err  = body.get('error', {})

        print "Status is: %s" % e.http_status
        print "Type is: %s" % err.get('type')
        print "Code is: %s" % err.get('code')
        # param is '' in this case
        print "Param is: %s" % err.get('param')
        print "Message is: %s" % err.get('message')
      except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        body = e.json_body
        err  = body.get('error', {})

        print "Status is: %s" % e.http_status
        print "Type is: %s" % err.get('type')
        print "Code is: %s" % err.get('code')
        # param is '' in this case
        print "Param is: %s" % err.get('param')
        print "Message is: %s" % err.get('message')
      except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        body = e.json_body
        err  = body.get('error', {})

        print "Status is: %s" % e.http_status
        print "Type is: %s" % err.get('type')
        print "Code is: %s" % err.get('code')
        # param is '' in this case
        print "Param is: %s" % err.get('param')
        print "Message is: %s" % err.get('message')
      except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        body = e.json_body
        err  = body.get('error', {})

        print "Status is: %s" % e.http_status
        print "Type is: %s" % err.get('type')
        print "Code is: %s" % err.get('code')
        # param is '' in this case
        print "Param is: %s" % err.get('param')
        print "Message is: %s" % err.get('message')
      except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        body = e.json_body

        err  = body.get('error', {})

        print "Status is: %s" % e.http_status
        print "Type is: %s" % err.get('type')
        print "Code is: %s" % err.get('code')
        # param is '' in this case
        print "Param is: %s" % err.get('param')
        print "Message is: %s" % err.get('message')
      except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        body = e.json_body
        err  = body.get('error', {})

        print "Status is: %s" % e.http_status
        print "Type is: %s" % err.get('type')
        print "Code is: %s" % err.get('code')
        # param is '' in this case
        print "Param is: %s" % err.get('param')
        print "Message is: %s" % err.get('message')
      except Exception as e:
        # Something else happened, completely unrelated to Stripe
        body = e.json_body
        err  = body.get('error', {})

        print "Status is: %s" % e.http_status
        print "Type is: %s" % err.get('type')
        print "Code is: %s" % err.get('code')
        # param is '' in this case
        print "Param is: %s" % err.get('param')
        print "Message is: %s" % err.get('message')

    user.is_active = False
    user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)

class PaymentAPIView(APIView):
  def post(self, request):
    print('Hello World')
    token = request.POST['stripeToken']

    # Does user have a stripe ID?
    if request.user.stripe_id: # If yes...
      print('I have a stripe id')
      try:
        print('Getting customer info')
        customer = stripe.Customer.retrieve(request.user.stripe_id)
        if  customer.deleted:
          print('Creating new customer')
          customer = createCustomer(request)
      except:
        # If stripe_id is deleted then create a new one
        print('do something else')
        # print(customer)
        

    else: # If not...
      print('I don\'t have a stripe id')

      # Create new customer for user
      customer = createCustomer(request) 
      
    # Update stripe id to user instance
    request.user.stripe_id = customer.id
    request.user.save()

    # Subscribe
    subscription = subscribe(request)
    request.user.subscription = subscription.id
    request.user.sub_end = subscription.current_period_end
    request.user.status = subscription.status
    request.user.save()
    return Response(status=status.HTTP_202_ACCEPTED)

    
  
  def delete(self, request):
    try:
      # does user have a valid subscription?
      subscription = stripe.Subscription.retrieve(request.user.subscription)
      print('This is the subscription')
      subscription.delete()
      request.user.status = 'canceled'
      request.user.subscription = None
      request.user.sub_end = None
      request.user.save()
    except Exception as e:
      print("ERROR")
      print(e)
      request.user.status = 'canceled'
      request.user.subscription = None
      request.user.sub_end = None
      request.user.save()
    return Response(status=status.HTTP_202_ACCEPTED)
        