from rest_framework import viewsets
from .models import (Receiver,
                     Channel,
                     Question,
                     Reply,
                     QuestionSet,
                     ReplySet)
from .serializers import (ReceiverSerializer,
                          ChannelSerializer,
                          QuestionSerializer,
                          ReplySerializer,
                          QuestionSetSerializer,
                          ReplySetSerializer)

class ReceiverViewSet(viewsets.ModelViewSet):
    queryset = Receiver.objects.all()
    serializer_class = ReceiverSerializer

class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

class QuestionSetViewSet(viewsets.ModelViewSet):
    queryset = QuestionSet.objects.all()
    serializer_class = QuestionSetSerializer

class ReplySetViewSet(viewsets.ModelViewSet):
    queryset = ReplySet.objects.all()
    serializer_class = ReplySetSerializer