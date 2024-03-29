# Generated by Django 5.0 on 2023-12-16 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ToDo_app', '0010_remove_todo_elapsed_time_remove_todo_start_time_and_more'),
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
