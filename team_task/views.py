from django.shortcuts import render, redirect
from accounts.models import CustomUser
from .models import ToDoItem, TaskAssignment
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserGroupForm, AddMemberForm
from .models import UserGroup
from django.views.decorators.http import require_http_methods

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt  # Це потрібно, якщо ви хочете використовувати csrf_exempt
import json
from django.db.models import Q
from django.contrib import messages

from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse


@login_required
@require_http_methods(['POST'])
def timers_task(request):
    task_id = request.POST.get('task_id')
    action = request.POST.get('action')

    if action == 'start':
        task = ToDoItem.objects.get(id=task_id)
        elapsed_time_task = calculate_time(task)
        assigned_user = task.assigned_to.user
        task.elapsed_time_task += elapsed_time_task
        task.start_time_task = timezone.now()
        task.save()
        return JsonResponse({'status': 'success', 'elapsed_time_task': elapsed_time_task})

    elif action == 'stop':
        task = ToDoItem.objects.get(id=task_id)
        elapsed_time_task = calculate_time(task)
        task.elapsed_time_task += elapsed_time_task
        task.start_time_task = None
        task.save()
        return JsonResponse({'status': 'success', 'elapsed_time_task': elapsed_time_task})

    elif action == 'pause':
        task = ToDoItem.objects.get(id=task_id)
        elapsed_time_task = calculate_time(task)
        return JsonResponse({'status': 'success', 'elapsed_time_task': elapsed_time_task})

    else:
        return JsonResponse({'status': 'error', 'message': 'Невірна дія'})

def calculate_time(task):
    if task.start_time_task:
        stop_time = timezone.now()
        elapsed_time_task = stop_time - task.start_time_task
        return int(elapsed_time_task.total_seconds())
    else:
        return 0


def list_user_groups(request):
    user_groups = UserGroup.objects.filter(creator=request.user).values('id', 'name')
    data = {'user_groups': list(user_groups)}
    return JsonResponse(data)

def get_users_for_group(request, group_id):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        users = CustomUser.objects.filter(user_groups=group_id).values('id', 'username', 'first_name', 'last_name')
        data = {'users': list(users)}
        return JsonResponse(data)
    return JsonResponse({'error': 'Invalid request'})

def create_task(request):
    if request.method == 'POST':
        user_group_id = request.POST.get('user_group')
        assigned_to_id = request.POST.get('assigned_to')
        title = request.POST.get('title')
        description = request.POST.get('description')

        # Отримання інформованої дати та часу з форми
        deadline_naive = request.POST.get('deadline')
        deadline_aware = timezone.make_aware(datetime.strptime(deadline_naive, '%Y-%m-%dT%H:%M'))

        # Перевірка на існування групи та чи користувач є створювачем групи
        try:
            user_group = UserGroup.objects.get(id=user_group_id, creator=request.user)
        except UserGroup.DoesNotExist:
            return JsonResponse({'error': 'Invalid user group'})

        # Отримання об'єкта користувача
        assigned_to = CustomUser.objects.get(id=assigned_to_id)

        # Створення об'єкта TaskAssignment
        task_assignment = TaskAssignment.objects.create(user=assigned_to, user_group=user_group)

        # Створення об'єкта ToDoItem з осведомленою датою та часом
        task = ToDoItem.objects.create(
            title=title,
            description=description,
            deadline=deadline_aware,
            assigned_to=task_assignment,
            created_by=request.user,
            is_complete=False
        )
        messages.success(request, 'Завдання успішно створено.')

        return JsonResponse({'success': True, 'task': {
            'title': task.title,
            'deadline': task.deadline.isoformat(),  # Перетворюємо дату у формат ISO
            'created_at': task.created_at.isoformat(),  # Перетворюємо дату у формат ISO
            'description': task.description,
            'assigned_to': {
                'first_name': task.assigned_to.user.first_name,
                'last_name': task.assigned_to.user.last_name,
            },
            'is_complete': task.is_complete,
        }})

    # Отримати всі завдання, створені користувачем
    created_tasks = ToDoItem.objects.filter(created_by=request.user).order_by('-created_at')
    unfinished_tasks_count = created_tasks.filter(is_complete=False).count()
    
    # Визначити номер поточної сторінки та кількість елементів на сторінці
    page = request.GET.get('page', 1)
    items_per_page = 5  # Ви можете вказати бажану кількість елементів на сторінці

    # Отримати пагінатор
    paginator = Paginator(created_tasks, items_per_page)

    try:
        # Отримати поточну сторінку
        current_page = paginator.page(page)
    except EmptyPage:
        # Якщо номер сторінки більше, ніж загальна кількість сторінок, повернути останню сторінку
        current_page = paginator.page(paginator.num_pages)
    

    return render(request, 'team_task/create_task.html', {'created_tasks': current_page, 'unfinished_tasks_count': unfinished_tasks_count})

def search(request):
    query = request.GET.get('q')
    print("Query:", query)

    # Ваш код для пошуку, наприклад, використовуючи Q-об'єкт
    if query:
        results = ToDoItem.objects.filter(Q(title__icontains=query, created_by=request.user))
    else:
        results = []
        
    return render(request, 'team_task/create_task.html', {'results': results, 'query': query})

def task_list(request):
    assigned_task_assignments = TaskAssignment.objects.filter(user=request.user)
    assigned_tasks = ToDoItem.objects.filter(assigned_to__in=assigned_task_assignments).order_by('-created_at')

    incoming_tasks_count = assigned_tasks.filter(is_complete=False).count()

    page = request.GET.get('page', 1)
    paginator = Paginator(assigned_tasks, 5)  # Ви можете вказати бажану кількість елементів на сторінці

    try:
        assigned_tasks = paginator.page(page)
    except PageNotAnInteger:
        assigned_tasks = paginator.page(1)
    except EmptyPage:
        assigned_tasks = paginator.page(paginator.num_pages)

    return render(request, 'team_task/task_list.html', {'assigned_tasks': assigned_tasks, 'incoming_tasks_count': incoming_tasks_count})

def search_tasks(request):
    query = request.GET.get('q')
    print("Query:", query)

    # Отримайте всі завдання, які призначені поточному користувачеві
    assigned_task_assignments = TaskAssignment.objects.filter(user=request.user)

    # Отримайте завдання через зовнішній ключ до TaskAssignment
    assigned_tasks = ToDoItem.objects.filter(assigned_to__in=assigned_task_assignments).order_by('-created_at')  

    # Ваш код для пошуку, наприклад, використовуючи Q-об'єкт
    if query:
        results_task = assigned_tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:
        results_task = []

    return render(request, 'team_task/task_list.html', {'results_task': results_task, 'query': query})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(ToDoItem, id=task_id, created_by=request.user)

    if request.method == 'POST':
        new_title = request.POST.get('new_title')
        new_description = request.POST.get('new_description')
        new_deadline = request.POST.get('new_deadline')

        # Оновити дані завдання
        task.title = new_title
        task.description = new_description

        # Перетворити новий дедлайн у формат datetime та зберегти
        task.deadline = timezone.make_aware(datetime.strptime(new_deadline, '%Y-%m-%dT%H:%M'))
        task.save()

        # Після збереження перенаправте користувача на початкову сторінку або куди вам потрібно
        return redirect('create_task')

    return render(request, 'team_task/create_task.html', {'task': task})

@login_required
def create_user_group(request):
    user_groups = UserGroup.objects.filter(creator=request.user)
    users = CustomUser.objects.all()  # Змініть це на ваш спосіб отримання списку користувачів


    if request.method == 'POST':
        form = UserGroupForm(request.POST)
        if form.is_valid():
            user_group = form.save(commit=False)
            user_group.creator = request.user
            user_group.save()
            form.save_m2m()
            return redirect('create_user_group')
    else:
        form = UserGroupForm()

    return render(request, 'team_task/create_user_group.html', {'form': form,  'user_groups': user_groups, 'users': users})



@login_required
def delete_task(request, task_id):
    if request.method == 'POST':
        try:
            task = ToDoItem.objects.get(id=task_id, created_by=request.user)
            task.delete()
            return JsonResponse({'success': True})
        except ToDoItem.DoesNotExist:
            return JsonResponse({'error': 'Invalid task'})
    return JsonResponse({'error': 'Invalid request'})

@login_required
def toggle_complete(request, todo_id):
    todo = ToDoItem.objects.get(id=todo_id)
    todo.is_complete = not todo.is_complete
    todo.save()
    return redirect(request.META['HTTP_REFERER'])


from django.shortcuts import get_object_or_404

from django.shortcuts import render, redirect, get_object_or_404

@login_required
def edit_user_group(request, group_id):
    user_group = get_object_or_404(UserGroup, pk=group_id, creator=request.user)
    
    if request.method == 'POST':
        form = UserGroupForm(request.POST, instance=user_group)
        if form.is_valid():
            form.save()
            return redirect('create_user_group')
    else:
        form = UserGroupForm(instance=user_group)
    
    return render(request, 'team_task/edit_user_group.html', {'form': form, 'group': user_group})

from django.shortcuts import get_object_or_404

@login_required
def delete_user_group(request, group_id):
    user_group = get_object_or_404(UserGroup, pk=group_id, creator=request.user)
    user_group.delete()
    return redirect('create_user_group')

@login_required
def add_member(request, group_id):
    user_group = get_object_or_404(UserGroup, pk=group_id, creator=request.user)
    
    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user']
            user_group.members.add(user_id)
    
    return redirect('edit_user_group', group_id=group_id)

@login_required
def remove_member(request, group_id, user_id):
    user_group = get_object_or_404(UserGroup, pk=group_id, creator=request.user)
    user = get_object_or_404(CustomUser, pk=user_id)
    user_group.members.remove(user)
    return redirect('edit_user_group', group_id=group_id)

