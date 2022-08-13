from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import auth

from customuser.forms import CustomUserSignUpForm, CustomUserLoginForm
from customuser.models import CustomUser


def index_view(request):
    return render(request, 'index.html')


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserSignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            form_to_save = form.save(commit=False)
            form_to_save.password = make_password(password)
            form_to_save.save()
            user = auth.authenticate(username=email, password=password)
            auth.login(request, user)
            return redirect('customuser:index')
    else:
        form = CustomUserSignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                messages.error(request, 'User with this e-mail does not exist')
                return render(request, 'login.html', {'form': form})

            username = user.email
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect('customuser:index')
            else:
                messages.error(request, 'Invalid Password')
    else:
        form = CustomUserLoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    auth.logout(request)
    return redirect('customuser:index')
