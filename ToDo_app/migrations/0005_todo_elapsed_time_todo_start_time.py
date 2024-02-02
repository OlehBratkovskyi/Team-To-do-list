# Generated by Django 5.0 on 2023-12-14 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ToDo_app', '0004_remove_todo_timer_seconds'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='elapsed_time',
            field=models.FloatField(default=0, verbose_name='Пройдений час'),
        ),
        migrations.AddField(
            model_name='todo',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Час старту'),
        ),
    ]
