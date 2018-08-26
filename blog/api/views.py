# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..models import Post
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import PostModelSerializer
from django.http import Http404
from ..forms import BlogPostForm
from django.utils import timezone
from django.shortcuts import get_object_or_404, get_list_or_404
import pprint

class PostAPIView(APIView):
  def get(self,request):
    data = Post.objects.all()
    serializer = PostModelSerializer(data, many=True)
    serialized_data = serializer.data
    return Response(serialized_data, status.HTTP_200_OK)

  def delete(self, request):
    if request.user.is_staff:
      post = get_object_or_404(Post,id=request.data['id'],author=request.user)
      post.delete();
      return Response(status=status.HTTP_202_ACCEPTED)
    else:
      return Response(status=status.HTTP_401_UNAUTHORIZED)

  def post(self, request):
    if request.user.is_staff:
      serializer = PostModelSerializer(data=request.data)
    
      if not serializer.is_valid():
        return Response(serializer.errors,
                          status=status.HTTP_400_BAD_REQUEST)
      else:
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
          post = form.save(commit=False)
          post.author = request.user
          post.published_date = timezone.now()
          post.save()
        serializer = PostModelSerializer(post)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    else:
      return Response(status=status.HTTP_401_UNAUTHORIZED)

  def put(self, request):
    data = request.POST
    post = get_object_or_404(Post,id=data['id'])
    form = BlogPostForm(request.POST, request.FILES, instance=post)
    if form.is_valid():
      form.save()
      serializer = PostModelSerializer(post)
      return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    else:
      return Response({'detail':'invalid form data'},status=status.HTTP_400_BAD_REQUEST)

  
