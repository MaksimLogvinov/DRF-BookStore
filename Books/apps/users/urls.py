from django.urls import path, include

from apps.users.views import (
    RegisterUserView, UserConfirmEmailView, EmailResetPasswordView,
    ResetPasswordView, ResetPasswordDone, )

urlpatterns = [
    path(
        'auth/',
        include('rest_framework.urls'),
    ),
    path(
        'register/',
        RegisterUserView.as_view(),
    ),
    path(
        'confirm-email/<str:uidb64>/<str:token>/',
        UserConfirmEmailView.as_view(),
        name='confirm_email'
    ),
    path(
        'reset-password/',
        ResetPasswordView.as_view(),
    ),
    path(
        'reset-password/<str:uidb64>/<str:token>/',
        EmailResetPasswordView.as_view(),
        name='password_email'
    ),
    path(
        'reset-password/<str:uidb64>/<str:token>/done/',
        ResetPasswordDone.as_view(),
        name='password_email'
    ),
]
