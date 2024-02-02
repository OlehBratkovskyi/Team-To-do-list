from django.urls import path, include
from . import views
from .views import get_users_for_group, delete_task, edit_task, timers_task

urlpatterns = [
    path('timers/', timers_task, name='timers_task'),
    path('create_task/', views.create_task, name='create_task'),
    path('delete_task/<int:task_id>/', delete_task, name='delete_task'),    
    path('get_users_for_group/<int:group_id>/', get_users_for_group, name='get_users_for_group'),
    path('edit_task/<int:task_id>/', edit_task, name='edit_task'), 
    path('toggle_complete/<int:todo_id>/', views.toggle_complete, name='toggle_complete'),
    path('create_user_group/', views.create_user_group, name='create_user_group'),
    path('list_user_groups/', views.list_user_groups, name='list_user_groups'),
    path('edit_user_group/<int:group_id>/', views.edit_user_group, name='edit_user_group'),
    path('delete_user_group/<int:group_id>/', views.delete_user_group, name='delete_user_group'),
    path('add_member/<int:group_id>/', views.add_member, name='add_member'),
    path('remove_member/<int:group_id>/<int:user_id>/', views.remove_member, name='remove_member'),
    path('task_list/', views.task_list, name='task_list'),
    path('search/', views.search, name='search'),
    path('search_tasks/', views.search_tasks, name='search_tasks'),
]