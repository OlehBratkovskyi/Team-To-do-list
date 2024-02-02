from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class ToDo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    title = models.CharField('Назва завдання', max_length=500)
    description = models.TextField('Опис завданяя', blank=True)
    created_at = models.DateTimeField('Створено', default=timezone.now)
    deadline = models.DateTimeField('Дедлайн', blank=True, null=True, default=timezone.now)
    is_complete = models.BooleanField('Виконано', default=False)
    start_time = models.DateTimeField('Час старту', blank=True, null=True)
    elapsed_time = models.FloatField('Пройдений час', default=0)

    class Meta:
        verbose_name = 'Завдання'
        verbose_name_plural = 'Завдання'

    def __str__(self):
        return self.title
    # Метод у вашому класі моделі
    def elapsed_time_formatted(self):
        hours, remainder = divmod(self.elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

        