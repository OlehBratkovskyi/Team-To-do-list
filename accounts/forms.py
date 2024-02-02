from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Обов'язкове поле.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Обов'язкове поле.")
    email = forms.EmailField(max_length=254, required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_picture', 'password1', 'password2']
