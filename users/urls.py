from django.urls import path, include, re_path
from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("register/", include("dj_rest_auth.registration.urls")),
    path("verify-email/", VerifyEmailView.as_view(), name="rest_verify_email"),
    path(
        "account-confirm-email/<str:key>/",
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    path(
        "account-confirm-email/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
]
