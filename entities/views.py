import tempfile
import xlsxwriter
import re

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages

from .models import QuestionSet, Question, ReplySet, Reply, Receiver
from .forms import QuestionSetModelForm, QuestionFormSet, ReceiverModelForm, AddSubscriberForm, ChannelModelForm

from webexteamssdk import WebexTeamsAPI

from pyadaptivecards.card import AdaptiveCard
from pyadaptivecards.components import TextBlock, Choice
from pyadaptivecards.inputs import Text, Choices


# Create your views here.

def get_card_from_question_set(qs):
    body = []
    intro = TextBlock(f"## {qs.name}")
    body.append(intro)

    # Create a input for each of the questions
    for q in qs.questions.all():
        input_id = f"{qs.id}#{q.id}"

        label = TextBlock(f"**{q.text}**")
        body.append(label)

        if q.question_type == Question.TYPE_TEXT:
            field = Text(input_id)
            body.append(field)
        elif q.question_type == Question.TYPE_MC:
            string_choices = re.search(r'\((.*?)\)', q.text).group(1).split(",")

            choices = []
            for str_choice in string_choices:
                c = Choice(str_choice, str_choice)
                choices.append(c)
            field = Choices(choices, input_id)
            body.append(field)

    submit_action = {
        'type': "Action.Submit",
        'title': "Send Survey", 
        'data': {
            'question_set': str(qs.id)
        }
    }

    card = AdaptiveCard(body=body, actions=[])

    ret = card.to_dict()
    ret['actions'].append(submit_action)

    return ret

class UserView(View):
    def get(self, request):
        ctx = {
            'receiver': Receiver.objects.all(),
            'receiver_form': ReceiverModelForm(),
            'add_subscriber_form': AddSubscriberForm(),
            'add_channel_form': ChannelModelForm()
        }

        return render(request, 'entities/create_user.html', context=ctx)

    def post(self, request):
        form = ReceiverModelForm(request.POST)

        if form.is_valid():
            obj = form.save()
            obj.save()

            return redirect('users')

class CreateChannelView(View):
    def post(self, request):
        f = ChannelModelForm(request.POST)

        if f.is_valid():
            obj = f.save()
            obj.save()

            messages.add_message(request, messages.SUCCESS, "Channel successfully created!")

            return redirect('users')

class CreateSubscriptionView(View):
    def post(self, request):
        f = AddSubscriberForm(request.POST)

        if f.is_valid():
            c = f.cleaned_data['channel']
            for r in f.cleaned_data['receivers']:
                c.receiver.add(r)

            return redirect('users')
         
class ListQuestionSetView(View):
    def get(self, request):
        ctx = {
            'question_sets': QuestionSet.objects.all()
        }

        return render(request, "entities/list_questionsets.html", context=ctx)

class ReportView(View):
    def get(self, request, question_set_id):
        qs = get_object_or_404(QuestionSet, pk=question_set_id)

        # Get replies
        reply_sets = ReplySet.objects.filter(question_set=qs)

        ctx = {
            'question_set': qs,
            'reply_sets': reply_sets
        }

        return render(request, "entities/report.html", context=ctx)

class DownloadReportView(View):
    def get(self, request, question_set_id):
        qs = get_object_or_404(QuestionSet, pk=question_set_id)

        reply_sets = ReplySet.objects.filter(question_set=qs)

        with tempfile.NamedTemporaryFile(suffix='.xlsx') as temp:
            workbook = xlsxwriter.Workbook(temp.name)
            worksheet = workbook.add_worksheet()

            bold = workbook.add_format({'bold': True})

            # Add excel header
            worksheet.write(0, 0, "Replier", bold)

            col = 1
            for q in qs.questions.all():
                worksheet.write(0, col, q.text, bold)

                col += 1
            
            row = 1
            for rs in reply_sets:
                worksheet.write(row, 0, str(rs.receiver))

                col = 1
                for q in qs.questions.all():
                    for r in rs.replies.all():
                        if r.question == q:
                            worksheet.write(row, col, r.text)

                            col += 1
                row += 1
            workbook.close()
            temp.flush()

            resp = HttpResponse(temp.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            
            file_name = self.__sanitize_name(qs.name)
            resp['Content-Disposition'] = f"attachment; filename={file_name}.xlsx"
            
            return resp

    def __sanitize_name(self, name):
        return str(name).replace(" ", "_").lower()


class SendQuestionSetView(View):
    def get(self, request, question_set_id):
        qs = get_object_or_404(QuestionSet, pk=question_set_id)

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
        return redirect('questions')


class CreateQuestionSetView(View):
    def get(self, request):
        ctx = {
            'question_set_form': QuestionSetModelForm(),
            'questions_form_set': QuestionFormSet(queryset=Question.objects.none())
        }

        return render(request, "entities/create_question.html", context=ctx)
    
    def post(self, request):
        qsf = QuestionSetModelForm(request.POST)
        questions_form_set = QuestionFormSet(request.POST)

        if qsf.is_valid() and questions_form_set.is_valid():
            qs = qsf.save()
            

            # Save all questions
            for qf in questions_form_set:
                q = qf.save()
                qs.questions.add(q)
            
            qs.save()
        
            return redirect('create.question')
        else:
            return HttpResponse(qsf.errors)