from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required

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
        return redirect('dashboard')
    return render(request, 'register.html')


def home(request):
    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('home')

