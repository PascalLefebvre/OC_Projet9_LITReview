from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render

from . import forms


def login_page(request):
    message = ''
    if request.method != 'POST':
        form = forms.LoginForm()
    else:
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                message = 'Identifiants invalides.'
    return render(
        request, 'accounts/login.html', context={'form': form, 'message': message})

def logout_user(request):
    logout(request)
    return redirect('accounts:login')

def signup(request):
    if request.method != 'POST':
        form = forms.SignupForm()
    else:
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

    context={'form': form}
    return render(request, 'accounts/signup.html', context)
