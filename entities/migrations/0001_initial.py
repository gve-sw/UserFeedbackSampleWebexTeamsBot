# Generated by Django 3.0.6 on 2020-05-20 15:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionSet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('channel', models.ManyToManyField(to='entities.Channel')),
                ('questions', models.ManyToManyField(to='entities.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Receiver',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('mail', models.CharField(max_length=250)),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=250)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entities.Question')),
            ],
        ),
        migrations.CreateModel(
            name='ReplySet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('question_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entities.QuestionSet')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entities.Receiver')),
                ('replies', models.ManyToManyField(to='entities.Reply')),
            ],
        ),
        migrations.AddField(
            model_name='channel',
            name='receiver',
            field=models.ManyToManyField(to='entities.Receiver'),
        ),
    ]
