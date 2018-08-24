from rest_framework import serializers
from ..models import Ticket, Comment, UpVote

class TicketModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Ticket
    fields = [
      'id',
      'type',
      'description',
      'status',
      'user',
      'modified',
      'votes'
    ]

class UpVoteModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = UpVote
    fields = [
      'ticket',
      'user',
    ]

class CommentModelSerializer(serializers.ModelSerializer):
  # id = serializers.IntegerField(read_only=True)
  class Meta:
    model = Comment
    fields = [
      'id',
      'ticket',
      'comment',
      'user',
      'submitted'
    ]