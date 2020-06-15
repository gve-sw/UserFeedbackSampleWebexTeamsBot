import uuid

from django.db import models

# Create your models here.
class Receiver(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mail = models.CharField(max_length=250)
    name = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.name} ({self.mail})"

class Channel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    receiver = models.ManyToManyField(Receiver, blank=True)

    def __str__(self):
        return f"{self.name}"

class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=250)

    TYPE_TEXT = "TEXT"
    TYPE_MC = "MC"
    TYPE_CHOICES = (
        (TYPE_TEXT, "Text"),
        (TYPE_MC, "Multiple Choice")
    )
    question_type = models.CharField(max_length=5, choices=TYPE_CHOICES, default=TYPE_TEXT)


class Reply(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)

class QuestionSet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    questions = models.ManyToManyField(Question)
    channel = models.ManyToManyField(Channel)
    was_send = models.BooleanField(default=False)
    is_recurring = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({len(self.questions.all())} questions)"

class ReplySet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    receiver = models.ForeignKey(Receiver, on_delete=models.CASCADE)
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    replies = models.ManyToManyField(Reply)

    def __str__(self):
        return f"{self.receiver} on {self.question_set}"

