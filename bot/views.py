from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View
from django.conf import settings

import json
from webexteamssdk import WebexTeamsAPI

from entities.models import Receiver, QuestionSet, ReplySet, Reply

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class CardReceiverView(View):
    def post(self, request):
        payload = json.loads(request.body.decode('utf-8'))
        
        api = WebexTeamsAPI(access_token=settings.WEBEX_ACCESS_TOKEN)
        # Get receiver
        person = api.people.get(payload['data']['personId'])

        receiver = Receiver.objects.filter(mail=person.emails[0]).first()

        attachment = api.attachment_actions.get(payload['data']['id'])

        # Get questionset 
        qs = get_object_or_404(QuestionSet, pk=attachment.inputs['question_set'])

        # Create reply set
        rs = ReplySet(receiver=receiver, question_set=qs)
        rs.save()
        for q in qs.questions.all():
            key = f"{qs.id}#{q.id}"
            answer = attachment.inputs[key]

            r = Reply(question=q, text=answer)
            r.save()
            rs.replies.add(r)
        rs.save()

        # Delete message
        api.messages.delete(payload['data']['messageId'])
        api.messages.create(toPersonId=person.id, markdown="Thank your for the submission")

        return JsonResponse({'success': True})
