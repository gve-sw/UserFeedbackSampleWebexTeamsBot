from django.conf import settings
from background_task import background
from webexteamssdk import WebexTeamsAPI
from entities.models import QuestionSet
from entities.views import get_card_from_question_set

import datetime as dt

@background(schedule=5)
def send_recurring():
    # Get all recurring question sets
    recurring_qs = QuestionSet.objects.filter(is_recurring=True)

    for qs in recurring_qs:
        # Get unique list of people to send message to 
        to = set()

        for c in qs.channel.all():
            for r in c.receiver.all():
                to.add(r.mail)
        
        # Create card
        card = get_card_from_question_set(qs)

        attachment = {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": card
        }


        # Send card to everyone in to list
        api = WebexTeamsAPI(access_token=settings.WEBEX_ACCESS_TOKEN)

        for mail in to:
            api.messages.create(toPersonEmail=mail, markdown="Card. View on desktop", attachments=[attachment,])
        qs.was_send = True
        qs.save()
        print("Send recurring question set {}".format(qs))