from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'register.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name
        )

        UserProfile.objects.create(
            user=user,
            user_type=user_type
        )

        login(request, user)
        messages.success(request, 'Registration successful! Welcome to Share4Care!')
        return redirect('home')
    return render(request, 'register.html')
def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('home')