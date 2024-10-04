from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from blog.models import FanClub

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save() and p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    fanclubs = FanClub.objects.filter(users=request.user)
    context = {'u_form': u_form,
               'p_form': p_form,
               'fanclubs': fanclubs}
    return render(request, 'users/profile.html', context)

def groups(request):
    pass

def data(request):
    pass

def user_profile(request, username):
    user = User.objects.get(username=username)
    fanclubs = FanClub.objects.filter(users=user)
    return render(request, 'users/user_profile.html', context={'enduser': user, 'fanclubs': fanclubs})
