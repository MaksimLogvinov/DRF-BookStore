from django.urls import path
from rest_framework import routers

from apps.users.views import (
    RegisterUserViewSet, EmailResetPasswordView,
    ResetPasswordView, ResetPasswordDoneView, ProfileUserViewSet,
    SecurityUserViewSet, DeleteUserViewSet, ResetPasswordFailedView,
    UserConfirmEmailView,
)

urlpatterns_users = [
    path(
        'reset-password/',
        ResetPasswordView.as_view(),
        name='password_email'
    ),
    path(
        'reset-password/<str:uidb64>/<str:token>',
        EmailResetPasswordView.as_view(),
        name='password_email'
    ),
    path(
        'reset-password/<str:uidb64>/done/',
        ResetPasswordDoneView.as_view(),
        name='success_reset'
    ),
    path(
        'reset-password/<str:uidb64>/failed/',
        ResetPasswordFailedView.as_view(),
        name='failed_reset'
    ),
    path(
        'confirm-email/<str:uidb64>/<str:token>/',
        UserConfirmEmailView.as_view(),
        name='confirm_email'
    )
]


users_router = routers.DefaultRouter()
users_router.register(
    r'register',
    RegisterUserViewSet,
    basename='user_register'
)
users_router.register(
    r'profile',
    ProfileUserViewSet,
    basename='user_profile'
)
users_router.register(
    r'security',
    SecurityUserViewSet,
    basename='user_security'
)
users_router.register(
    r'delete',
    DeleteUserViewSet,
)

urlpatterns_users += users_router.urls
