from django.core.management.base import BaseCommand, CommandError
from entities.tasks import send_recurring
from webexteamssdk import WebexTeamsAPI
from background_task.models import Task

import datetime as dt

class Command(BaseCommand):
    help = 'Initialize repetition of the tasks'

    def handle(self, *args, **options):
        repeat_until_date = dt.datetime(2024, 12, 31)

        send_recurring(repeat=Task.WEEKLY, repeat_until=repeat_until_date)
        