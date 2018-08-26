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
from pprint import pprint

stripe.api_key = settings.STRIPE_SECRET

# >user auth managment
class UserAuthAPIView(APIView):
  permission_classes = ()
  def post(self, request):
    # print request.data['email']
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
          user = auth.authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
          if user is not None:
            auth.login(request, user)
          else:
            return Response({'detail':'invalid email and/or password'},status=status.HTTP_400_BAD_REQUEST)
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
      return Response({'detail':'unknown error'},status=status.HTTP_400_BAD_REQUEST)
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
        pprint(repr(body))
        pprint(dir(body))

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


      

  
