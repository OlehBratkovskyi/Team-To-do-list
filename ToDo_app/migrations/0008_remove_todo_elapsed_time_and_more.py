# Generated by Django 5.0 on 2023-12-16 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ToDo_app', '0007_todo_elapsed_time_todo_is_timer_running_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='elapsed_time',
        ),
        migrations.RemoveField(
            model_name='todo',
            name='is_timer_running',
        ),
        migrations.RemoveField(
            model_name='todo',
            name='start_time',
        ),
    ]
