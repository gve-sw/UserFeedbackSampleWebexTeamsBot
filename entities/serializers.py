from rest_framework import serializers
from .models import (Receiver,
                     Channel,
                     Question,
                     Reply,
                     QuestionSet,
                     ReplySet)

class ReceiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receiver
        fields = ['mail', 'name']

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['name', 'receiver']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['text', 'question_type']

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['question', 'text']

class QuestionSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionSet
        fields = ['name', 'questions', 'channel', 'was_send']

class ReplySetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplySet
        fields = ['receiver', 'question_set', 'replies']