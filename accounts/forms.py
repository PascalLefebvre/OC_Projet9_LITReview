from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='', widget=forms.TextInput(attrs={'size': 64, 'placeholder': "Nom d'utilisateur"}))
    password = forms.CharField(max_length=63, label='', widget=forms.PasswordInput(attrs={'size': 64, 'placeholder': 'Mot de passe'}))


class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=63, label='', widget=forms.TextInput(attrs={'size': 64, 'placeholder': "Nom d'utilisateur"}))
    password1 = forms.CharField(max_length=63, label='', widget=forms.PasswordInput(attrs={'size': 64, 'placeholder': 'Mot de passe'}))
    password2 = forms.CharField(max_length=63, label='', widget=forms.PasswordInput(attrs={'size': 64, 'placeholder': 'Confirmer le mot de passe'}))
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
