# urls.py
from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.register, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
]
