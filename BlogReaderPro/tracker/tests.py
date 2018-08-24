# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import Ticket,Comment,UpVote
from accounts.models import User

class TicketTestCase(TestCase):
  def setUp(self):
    user = User.objects.create(email='JessAnn@example.com')
    Ticket.objects.create(type="FEATURE", description="I would like this feature", user=user)

  def test_ticket_creation(self):
    ticket = Ticket.objects.get(description="I would like this feature")
    self.assertEqual(ticket.description, 'I would like this feature')

class VoteTestCase(TestCase):
  def setUp(self):
    user = User.objects.create(email='JessAnn@example.com')
    ticket = Ticket.objects.create(type="FEATURE", description="I would like this feature", user=user)
    UpVote.objects.create(ticket=ticket, user=user)

  def test_vote_creation(self):
    user = User.objects.get(email='JessAnn@example.com')
    ticket = Ticket.objects.get(type="FEATURE", description="I would like this feature", user=user)
    vote = UpVote.objects.get(user=user,ticket=ticket)

    self.assertEqual(vote.id, 1)
    self.assertEqual(vote.user.email, 'JessAnn@example.com')
    self.assertEqual(vote.ticket.description, "I would like this feature")

class CommentTestCase(TestCase):
  def setUp(self):
    user = User.objects.create(email='JessAnn@example.com')
    ticket = Ticket.objects.create(type="BUG", description="I hate this bug", user=user)
    Comment.objects.create(ticket=ticket, user=user, comment="Cucumbers taste good pickled.")

  def test_comment_creation(self):
    user = User.objects.get(email='JessAnn@example.com')
    ticket = Ticket.objects.get(type="BUG", description="I hate this bug", user=user)
    comment = Comment.objects.get(user=user,ticket=ticket)

    self.assertEqual(comment.id, 1)
    self.assertEqual(comment.ticket.id, 1)
    self.assertEqual(comment.user.email, 'JessAnn@example.com')
    self.assertEqual(comment.comment, 'Cucumbers taste good pickled.')
    