from django import forms
from .models import ToDoItem  # Імпортуємо модель завдань
from accounts.models import CustomUser  # Імпортуємо модель користувача
from .models import UserGroup
from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget
from .models import TaskAssignment

class CustomUserSelect2MultipleWidget(ModelSelect2MultipleWidget):
    def label_from_instance(self, user):
        return f"{user.username} ({user.first_name} {user.last_name})"


class UserGroupForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=CustomUserSelect2MultipleWidget(
            model=CustomUser,
            search_fields=['username__icontains'],
            attrs={
                'data-placeholder': 'Виберіть користувачів',
                'data-minimum-input-length': 0,
                'style': 'width: 100%;',
            },
        ),
    )

    class Meta:
        model = UserGroup
        fields = ('name', 'members',)


class EditUserGroupForm(forms.ModelForm):
    class Meta:
        model = UserGroup
        fields = ['name']  # Додайте інші поля, якщо потрібно

class AddMemberForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        widget=ModelSelect2MultipleWidget(
            model=CustomUser,
            search_fields=['username__icontains'],
            attrs={
                'data-placeholder': 'Виберіть користувача',
                'data-minimum-input-length': 0,
                'style': 'width: 100%;',
            },
        ),
    )

class RemoveMemberForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput())