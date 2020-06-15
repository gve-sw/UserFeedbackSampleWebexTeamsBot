from django.contrib import admin

# Register your models here.
from .models import (Receiver,
                     Channel,
                     Reply,
                     ReplySet,
                     Question,
                     QuestionSet)

admin.site.register(Receiver)
admin.site.register(Channel)
admin.site.register(Reply)
admin.site.register(ReplySet)
admin.site.register(Question)
admin.site.register(QuestionSet)