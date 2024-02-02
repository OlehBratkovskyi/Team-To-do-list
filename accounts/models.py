from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='accounts/profile_pictures/', null=True, blank=True)
    groups = models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='customuser_set', related_query_name='user')
    user_permissions = models.ManyToManyField(Permission, verbose_name='user permissions', blank=True, related_name='customuser_set', related_query_name='user')
    

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'