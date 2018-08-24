# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import User

# Create your tests here.
class UserModelTests(TestCase):
  def test_user_model(self):
    User(username="SteveJobs", password="1infiniteloop").save()
    self.assertEqual(User.objects.all().filter(username="SteveJobs").exists(), True)
    self.assertEqual(User.objects.all().filter(username="SteveMartin").exists(), False)