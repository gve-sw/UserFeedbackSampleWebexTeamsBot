from django import forms

from .models import (QuestionSet,
                     Question,
                     Receiver,
                     Channel)

class AddSubscriberForm(forms.Form):
    channel = forms.ModelChoiceField(Channel.objects.all())
    receivers = forms.ModelMultipleChoiceField(Receiver.objects.all())
    
class ReceiverModelForm(forms.ModelForm):
    class Meta:
        model = Receiver
        fields = ('mail', 'name')

class ChannelModelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ('name',)

class QuestionSetModelForm(forms.ModelForm):
    class Meta:
        model = QuestionSet
        fields = ('name', 'channel', 'is_recurring')

QuestionFormSet = forms.modelformset_factory(
    Question,
    fields=('text', 'question_type'),
    extra=1,
    widgets = {
        'text': forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Text displayed in the card',
            }
        )
    }
)