from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, UserUpdateForm, ProfilUpdateForm
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            
            if User.objects.filter(email=email).exists():
                messages.error(request,"Cette email est déjà utilisé. Veuillez en choisir une autre.")
                return render(request, 'user/register.html', {'form':form})
            
            form.save()
            name = form.cleaned_data.get('username')
            messages.success(request, f'Acount has been created for {name} continue to login')
            return redirect('user-login')
    else:
        form = CreateUserForm()  
    context = {
        'form':form
    }
    return render(request, 'user/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('user-logoutpage')


def deconnexion(request):
    return render(request, 'user/logout.html')


def profil(request):
    return render(request, 'user/profile.html')


def profil_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance = request.user)
        profile_form = ProfilUpdateForm(request.POST, request.FILES, instance= request.user.profil)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('user-profile')
    else:
        user_form = UserUpdateForm(instance = request.user)
        profile_form = ProfilUpdateForm(instance = request.user.profil)
    context = {
        'user_form':user_form,
        'profile_form':profile_form,
    }
    return render(request, 'user/profile_update.html', context)