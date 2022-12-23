""" Defines URL patterns for accounts. """

from django.urls import path, include

from . import views

app_name = "accounts"

urlpatterns = [
    # Login page
    path('', views.login_page, name='login'),
    # Logout page
    path('accounts/logout/', views.logout_user, name='logout'),
    # Registration page
    path("accounts/signup/", views.signup, name="signup"),
]
