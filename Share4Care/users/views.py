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


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'user_profile': user_profile})


@login_required




@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        request.user.first_name = request.POST.get('name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()

        user_profile.phone = request.POST.get('phone', '')
        user_profile.city = request.POST.get('city', '')
        user_profile.address = request.POST.get('address', '')

        if request.FILES.get('profile_picture'):

            if user_profile.profile_picture:
                old_pic_path = os.path.join(settings.MEDIA_ROOT, str(user_profile.profile_picture))
                if os.path.exists(old_pic_path):
                    os.remove(old_pic_path)

            # EITA NOTUN CHOBI SAVE KORAR JONNO
            user_profile.profile_picture = request.FILES['profile_picture']

        user_profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    return render(request, 'edit_profile.html', {'user_profile': user_profile})



@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(old_password):
            messages.error(request, 'Current password is incorrect!')
            return render(request, 'change_password.html')

        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match!')
            return render(request, 'change_password.html')

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Password changed successfully!')
        return redirect('dashboard')

    return render(request, 'change_password.html')