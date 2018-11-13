# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from .models import Post
from .forms import BlogPostForm
from django.contrib.auth.decorators import login_required
from helper.helper import check
  
# >posts_view
def posts_view(request):
  if not check(request):
    return redirect(reverse('accounts:logout'))
  posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
  return render(request, "blog/posts.html", {'posts': posts})
  
# >post_detail
def post_detail(request, id):
  if not check(request):
    return redirect(reverse('accounts:logout'))
  post = get_object_or_404(Post, pk=id)
  post.views += 1
  post.save()
  return render(request, "blog/postdetail.html", {'post': post})

# >new_post
@login_required(login_url='accounts:login')
def new_post(request):
  if not check(request):
    return redirect(reverse('accounts:logout'))
  # only staff can make blog posts
  if not request.user.is_staff:
    return redirect('blog:postlist')
  form = BlogPostForm()
  return render(request, 'blog/blogpostform.html', {'form': form})

# >edit_post
@login_required(login_url='accounts:login')
def edit_post(request, id):
  if not check(request):
    return redirect(reverse('accounts:logout'))
  # only staff can make blog posts
  if not request.user.is_staff:
    return redirect('blog:postlist')
  post = get_object_or_404(Post, pk=id)
  form = BlogPostForm(instance=post)
  return render(request, 'blog/blogpostform.html', {'form': form, 'id':id})
