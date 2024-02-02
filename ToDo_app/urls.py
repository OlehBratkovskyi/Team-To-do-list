from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add, name='add'),
    path('update/<int:todo_id>/', views.update, name='update'),
    path('delete/<int:todo_id>/', views.delete, name='delete'),
    path('edit/<int:todo_id>/', views.edit, name='edit'),
    # path('search_view/', views.search_view, name='search_view'),
    # path('search_ajax/', views.search_ajax, name='search_ajax'),
    # path('search/', views.search, name='search'),
    path('search_view/', views.search_view, name='search_view'),
    path('stopwatch/', views.stopwatch_actions, name='stopwatch_actions'),
]