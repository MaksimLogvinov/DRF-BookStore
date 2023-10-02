from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

from apps.users.views import (
    RegisterUserView, UserConfirmEmailView, EmailResetPasswordView,
    ResetPasswordView, ResetPasswordDone, ProfileUserView, SecurityUserView,
    DeleteUser, )

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path(r'^$', schema_view),
    path(
        'auth/',
        include('rest_framework.urls'),
    ),
    path(
        'register/',
        RegisterUserView.as_view(),
    ),
    path(
        "profile/",
        ProfileUserView.as_view(),
        name="profile_user"
    ),
    path(
        "security/",
        SecurityUserView.as_view(),
        name="security_user"
    ),
    path(
        "delete/",
        DeleteUser.as_view(),
        name='delete_user',
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
