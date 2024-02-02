from django.db import models
from django.conf import settings
from accounts.models import CustomUser  # Імпортуємо модель користувача
from django.contrib.auth.models import Group

class UserGroup(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(CustomUser, related_name='user_groups')
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class TaskAssignment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} - {self.user_group.name}"

class ToDoItem(models.Model):
    title = models.CharField('Назва завдання', max_length=100)
    description = models.TextField('Опис', blank=True)
    deadline = models.DateTimeField('Дедлайн')
    assigned_to = models.ForeignKey(TaskAssignment, on_delete=models.CASCADE, related_name='assigned_tasks', verbose_name='Призначити користувача')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_tasks', verbose_name='Створено користувачем')
    is_complete = models.BooleanField('Завершено', default=False)
    created_at = models.DateTimeField('Створено', auto_now_add=True)
    start_time_task = models.DateTimeField('Час старту', blank=True, null=True)
    elapsed_time_task = models.FloatField('Пройдений час', default=0)

    class Meta:
        verbose_name = 'Завдання для користувача'
        verbose_name_plural = 'Завдання для користувача'
    
        # Метод у вашому класі моделі
    def elapsed_time_task_formatted(self):
        hours, remainder = divmod(self.elapsed_time_task, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))