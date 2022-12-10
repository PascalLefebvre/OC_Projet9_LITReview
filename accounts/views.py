from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect, render

from . import forms


def register(request):
    if request.method != 'POST':
        form = forms.SignupForm()
    else:
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

    context={'form': form}
    return render(request, 'registration/register.html', context)
