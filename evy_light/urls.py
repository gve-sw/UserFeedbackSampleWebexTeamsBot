"""evy_light URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from entities import views as EntitieViews
from entities import api_views as ApiViews

from bot import views as BotViews

# Setup API routing
router = routers.DefaultRouter()
router.register(r'receivers', ApiViews.ReceiverViewSet)
router.register(r'channels', ApiViews.ChannelViewSet)
router.register(r'question_sets', ApiViews.QuestionSetViewSet)
router.register(r'replies', ApiViews.ReplyViewSet)
router.register(r'questions', ApiViews.QuestionViewSet)
router.register(r'reply_sets', ApiViews.ReplySetViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v0/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('webhooks/attachmentActions', BotViews.CardReceiverView.as_view(), name='webhook.attachmentActions'),
    path('receiver', EntitieViews.UserView.as_view(), name='users'),
    path('channel/create', EntitieViews.CreateChannelView.as_view(), name='create.channel'),
    path('subscription/create', EntitieViews.CreateSubscriptionView.as_view(), name='create.subscription'),
    path('questions/create', EntitieViews.CreateQuestionSetView.as_view(), name='create.question'),
    path('questions', EntitieViews.ListQuestionSetView.as_view(), name='questions'),
    path('questions/<str:question_set_id>/send', EntitieViews.SendQuestionSetView.as_view(), name='send.question'),
    path('questions/<str:question_set_id>/report', EntitieViews.ReportView.as_view(), name='report.questions'),
    path('questions/<str:question_set_id>/download', EntitieViews.DownloadReportView.as_view(), name='download.questions')
]
