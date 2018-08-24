# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..models import Ticket, UpVote, Comment
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import TicketModelSerializer, UpVoteModelSerializer, CommentModelSerializer
from accounts.models import User
from django.shortcuts import get_object_or_404, get_list_or_404
from django.core import serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# from rest_framework.permissions import IsAdminUser
# from rest_framework import permissions
# from pprint import pprint


class TicketAPI(APIView):
  permission_classes = (IsAuthenticatedOrReadOnly,)
  def get(self,request):
    if request.GET.has_key('page'):
      index = int(request.GET.get('page')) * 10
      if index > 10:
        data = Ticket.objects.all()[index - 10:index]
      else:
        data = Ticket.objects.all()[0:10]
    else:  
      data = get_list_or_404(Ticket)
    serializer = TicketModelSerializer(data,many=True)
    serialized_data = serializer.data
    return Response(serialized_data,status=status.HTTP_200_OK)

  def post(self, request):
    print request.POST
    user = get_object_or_404(User, id=request.user.id)
    if request.POST.get('type') == 'FEATURE' and not user.subscription:
      return Response(status=status.HTTP_402_PAYMENT_REQUIRED)
    serializer = TicketModelSerializer(data=request.data)
    if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
      data = serializer.data
      user = User.objects.get(id=request.user.id)

      ticket = Ticket.objects.create(type=data["type"],description=data["description"],user=user)

      ticket.status = "TODO"
      ticket.save()
      serializer = TicketModelSerializer(ticket)
      # return redirect('accounts:profile')
      return Response(serializer.data,status.HTTP_200_OK)

class VoteAPI(APIView):
  def post(self, request):
    ticket = get_object_or_404(Ticket, id=request.POST.get('ticket'))
    user = get_object_or_404(User, id=request.user.id)

    if ticket.type == 'FEATURE' and not user.subscription:
      return Response(status=status.HTTP_402_PAYMENT_REQUIRED)

    serializer = UpVoteModelSerializer(data=request.data)
    if not serializer.is_valid():
      return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    else:
      data = serializer.data
     
      vote = UpVote.objects.filter(ticket=data['ticket'], user=user)     
      # ticket = ticket = get_object_or_404(Ticket,id=data['ticket'])

      if not vote:
        vote = UpVote.objects.create(ticket=ticket, user=user)
        # vote.save()
      else:
        vote.delete()
      vote = UpVote.objects.filter(ticket=data['ticket'])
      ticket.votes = vote.count()
      ticket.save()
      return Response(status=status.HTTP_201_CREATED)

class CommentAPI(APIView):
  def post(self, request):
    print request.POST
    # user = get_object_or_404(User, id=request.user.id)
    # if ticket.type == 'FEATURE' and not user.subscription:
    #   return Response(status=status.HTTP_402_PAYMENT_REQUIRED)

    serializer = CommentModelSerializer(data=request.data)
    if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
      data = serializer.data
      user = get_object_or_404(User, id=request.user.id)
      # comment = Comment.objects.filter(ticket=data['ticket'], user=user)
      # pprint(dir(vote))
      # print vote.count()      
      ticket = ticket = get_object_or_404(Ticket,id=data['ticket'])
      
      comment = Comment.objects.create(ticket=ticket,comment=data['comment'],user=user)
      # comment.save()
      return Response(CommentModelSerializer(comment).data,status=status.HTTP_200_OK)

  def put(self, request):
    serializer = CommentModelSerializer(data=request.data)
    if not serializer.is_valid():
      return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    elif not request.data.has_key('id'):
      return Response('"id" field is required', status=status.HTTP_400_BAD_REQUEST)
    else:
      data = serializer.data
      user = get_object_or_404(User, id=request.user.id)
      comment = get_object_or_404(Comment, id=request.data['id'],user=user)
      comment.comment = data['comment']
      comment.save()
      return Response(CommentModelSerializer(comment).data['id'],status=status.HTTP_201_CREATED)

  def delete(self, request):
    user = get_object_or_404(User, id=request.user.id)
    comment = get_object_or_404(Comment, id=request.data['id'],user=user)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    