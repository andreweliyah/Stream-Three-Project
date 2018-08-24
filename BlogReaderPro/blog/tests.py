# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import Post
from accounts.models import User

class PostTestCase(TestCase):
  def setUp(self):
    user = User.objects.create(email='JessAnn@example.com')
    Post.objects.create(title="How to run a Django test", content="With test.py", author=user)

  def test_blog_post_creation(self):
    post = Post.objects.get(content="With test.py")
    self.assertEqual(post.content, "With test.py")
    