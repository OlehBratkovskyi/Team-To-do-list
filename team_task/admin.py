from django.contrib import admin
from .models import ToDoItem, UserGroup


# Register your models here.

admin.site.register(ToDoItem)
admin.site.register(UserGroup)