from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from .models import CustomUser
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')  # Перенаправити на сторінку входу
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')

        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password and new_password == confirm_password:
            user.set_password(new_password)
            messages.success(request, 'Пароль змінено успішно.')
        elif new_password:
            messages.error(request, 'Паролі не співпадають.')
        
        user.save()
        return redirect('profile')

    return render(request, 'registration/profile.html', {'user': user})