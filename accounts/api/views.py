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
from django.conf import settings
from pprint import pprint

stripe.api_key = settings.STRIPE_SECRET

class UserCreateAPIView(APIView):
  permission_classes = ()
  # Create new user
  def post(self, request):
    serializer = UserModelSerializer(data=request.data)
    if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
      data = serializer.data
      user = User.objects.create(email=data["email"])
      user.set_password(data["password"])
      user.save()
      return Response(serializer.data,status=status.HTTP_201_CREATED)

class UserListAPIView(APIView):
  def delete(self, request):
    try:
      request.user.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
    except:
      return Response(status=status.HTTP_404_NOT_FOUND)

  def put(self, request):
    data = request.data
    try:
      user = User.objects.get(email=data["email"])
    except User.DoesNotExist:
      return Response({"detail":"User Does Not Exist."},status=status.HTTP_400_BAD_REQUEST)
    if user.check_password(data['password']):
      user.set_password(data["newpassword"])
      user.save()
      return Response(status=status.HTTP_202_ACCEPTED)
    else:
      return Response(status=status.HTTP_401_UNAUTHORIZED)

# class UserPaymentAPIView(APIView):
#   def post(self, request):
#     # pprint(repr(status))
#     # pprint(dir(status))
#     # return Response(status=status.HTTP_202_ACCEPTED)
#     user = get_object_or_404(User,id=request.user.id)
#     # try:
#       # Create a Customer:
#       customer = stripe.Customer.create(
#         source=request.POST['stripeToken'],
#         email=user.email,
#       )
#       # Save customer id to stripe id of user:
#       user.stripe_id = customer.id
#       user.save()
#       # Charge the Customer:
#       charge = stripe.Charge.create(
#         amount=999,
#         currency='usd',
#         description='Dev Tracker Premium',
#         customer=customer.id,
#         statement_descriptor='Dev Tracker Subscription',
#       )
#     # return Response(status=status.HTTP_202_ACCEPTED)
#     # except Exception:
#       # pprint(repr(Exception.message))
#       # pprint(dir(Exception.message))
#       # print Exception.message
#       # return Response(status=status.HTTP_429_TOO_MANY_REQUESTS)

      

  
