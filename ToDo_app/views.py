from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import ToDo
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse

@login_required
@require_http_methods(['POST'])
def stopwatch_actions(request):
    todo_id = request.POST.get('todo_id')
    action = request.POST.get('action')

    if action == 'start':
        todo = ToDo.objects.get(id=todo_id)
        elapsed_time = calculate_elapsed_time(todo)
        todo.elapsed_time += elapsed_time
        todo.start_time = timezone.now()
        todo.save()
        return JsonResponse({'status': 'success', 'elapsed_time': elapsed_time})

    elif action == 'stop':
        todo = ToDo.objects.get(id=todo_id)
        elapsed_time = calculate_elapsed_time(todo)
        todo.elapsed_time += elapsed_time
        todo.start_time = None
        todo.save()
        return JsonResponse({'status': 'success', 'elapsed_time': elapsed_time})

    elif action == 'pause':
        todo = ToDo.objects.get(id=todo_id)
        elapsed_time = calculate_elapsed_time(todo)
        return JsonResponse({'status': 'success', 'elapsed_time': elapsed_time})

    else:
        return JsonResponse({'status': 'error', 'message': 'Невірна дія'})

@login_required
def calculate_elapsed_time(todo):
    if todo.start_time:
        stop_time = timezone.now()
        elapsed_time = stop_time - todo.start_time
        return int(elapsed_time.total_seconds())
    else:
        return 0
@login_required
def index(request):
    if request.user.is_authenticated:
        # Фільтруємо завдання для поточного користувача за полем 'user'
        todos = ToDo.objects.filter(user=request.user).order_by('-created_at')
        incomplete_tasks_count = todos.filter(is_complete=False).count()  # Лічильник незавершених завдань
        paginator = Paginator(todos, 5)
        page = request.GET.get('page')
        paginated_todos = paginator.get_page(page)
        return render(request, 'ToDoapp/index.html', {'todo_list': paginated_todos, 'title': 'Головна сторінка', 'incomplete_tasks_count': incomplete_tasks_count})
    else:
        return redirect('login')

@login_required
@require_http_methods(['POST'])
def add(request):
    if request.user.is_authenticated:
        title = request.POST['title']
        description = request.POST['description']
        deadline_str = request.POST['deadline']  
        deadline_str = request.POST.get('deadline')

        # Перевіряємо, чи не порожній рядок
        if deadline_str:
            
            deadline = timezone.datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
        else:
            deadline = None

        todo = ToDo(title=title, description=description, deadline=deadline, user=request.user)
        todo.save()
        return redirect('index')
    else:
        return redirect('login')

@login_required
def update(request, todo_id):
    
    todo = ToDo.objects.get(id=todo_id)
    todo.is_complete = not todo.is_complete
    todo.save()
    return redirect(request.META['HTTP_REFERER'])

@login_required
def delete(request, todo_id):
    todo = ToDo.objects.get(id=todo_id)
    todo.delete()
    return redirect('index')

@login_required
def edit(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id)

    if request.method == 'POST':
        new_title = request.POST.get('new_title')
        new_description = request.POST.get('new_description')
        new_deadline_str = request.POST.get('new_deadline')  # Отримати новий дедлайн з POST-запиту
        new_deadline = None

        # Перевіряємо, чи не порожній рядок
        if new_deadline_str:
            # Ваш формат має бути '%Y-%m-%dT%H:%M', а не '%Y-%m-%d %H:%M:%S'
            new_deadline = timezone.datetime.strptime(new_deadline_str, '%Y-%m-%dT%H:%M')

        todo.title = new_title
        todo.description = new_description
        todo.deadline = new_deadline  # Оновлюємо дедлайн
        todo.save()

        return redirect('index')

    return render(request, 'ToDoapp/edit.html', {'todo': todo})


@login_required
def search_view(request):
    query = request.GET.get('q')
    print("Query:", query)
    # Ваш код для пошуку, наприклад, використовуючи Q-об'єкт
    if query:
        results = ToDo.objects.filter(Q(title__icontains=query, user=request.user))
    else:
        results = []
        
    return render(request, 'ToDoapp/index.html', {'results': results, 'query': query})
