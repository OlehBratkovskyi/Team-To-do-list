# Generated by Django 5.0 on 2023-12-16 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ToDo_app', '0009_todo_elapsed_time_todo_start_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='elapsed_time',
        ),
        migrations.RemoveField(
            model_name='todo',
            name='start_time',
        ),
        migrations.AlterField(
            model_name='todo',
            name='description',
            field=models.TextField(blank=True, verbose_name='Опис завданяя'),
        ),
    ]
