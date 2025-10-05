from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("exam/", views.exam, name="exam"),
    path("submit/", views.submit, name="submit"),
    path("result/<int:submission_id>/", views.result, name="result"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("", views.exam, name="home"),
]
