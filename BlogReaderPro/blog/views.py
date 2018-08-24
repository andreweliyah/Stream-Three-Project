# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post

# Create your views here.
# >posts_view
def posts_view(request):
  posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
  return render(request, "blog/posts.html", {'posts': posts})
  
# >post_detail
def post_detail(request, id):
  post = get_object_or_404(Post, pk=id)
  post.views += 1
  post.save()
  return render(request, "blog/postdetail.html", {'post': post})