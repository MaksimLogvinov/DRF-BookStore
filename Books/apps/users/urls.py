from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from apps.users.views import (
    RegisterUserViewSet, UserConfirmEmailViewSet, EmailResetPasswordViewSet,
    ResetPasswordViewSet, ResetPasswordDoneViewSet, ProfileUserViewSet,
    SecurityUserViewSet, DeleteUserViewSet, ResetPasswordFailedViewSet
)

schema_view = get_swagger_view(title='Users API')

users_router = routers.SimpleRouter()
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
    basename='user_delete'
)
users_router.register(
    r'confirm-email/<str:uidb64>/<str:token>',
    UserConfirmEmailViewSet,
    basename='user_confirm_email'
)
users_router.register(
    r'reset-password',
    ResetPasswordViewSet,
    basename='reset_password'
)
users_router.register(
    r'reset-password/<str:uidb64>/<str:token>',
    EmailResetPasswordViewSet,
    basename='validation_reset_password'
)
users_router.register(
    r'reset-password/<str:uidb64>/<str:token>/done',
    ResetPasswordDoneViewSet,
    basename='success_reset'
)
users_router.register(
    'reset-password/<str:uidb64>/<str:token>/failed',
    ResetPasswordFailedViewSet,
    basename='failed_reset'
)

urlpatterns = users_router.urls
