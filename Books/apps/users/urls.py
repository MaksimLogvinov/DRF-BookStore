from django.urls import path, include

from apps.users.views import (
    RegisterUserView, UserConfirmEmailView, )

urlpatterns = [
    path(
        'auth/',
        include('rest_framework.urls'),
        name='auth'
    ),
    path(
        "register/",
        RegisterUserView.as_view(),
        name="register"
    ),
    path(
        "confirm-email/<str:uidb64>/<str:token>/",
        UserConfirmEmailView.as_view(),
        name="confirm_email"
    ),
]
