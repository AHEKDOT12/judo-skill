from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render


def redirect_by_role(user):
    if hasattr(user, 'profile'):
        if user.profile.role == 'coach':
            return redirect('dojo:coach_dashboard')

        if user.profile.role == 'student':
            return redirect('dojo:student_my_profile')

    if user.is_superuser:
        return redirect('/admin/')

    return redirect('dojo:index')


def login_view(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect_by_role(user)

        messages.error(request, 'Неверный логин или пароль.')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('dojo:index')