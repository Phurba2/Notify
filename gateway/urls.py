from django.urls import path

from .views import (
    NotifyView,
    webhook_receiver,
    ProfessionalSignupView,
    ProfessionalVerifyOTPView,
    ForgotPasswordRequestView,
    VerifyForgotPasswordOTPView,
    ResetPasswordView,
)


urlpatterns = [
    path("notify", NotifyView.as_view(), name="notify"),
    path("webhook-receiver/", webhook_receiver, name="webhook_receiver"),
    path("professional-signup", ProfessionalSignupView.as_view(), name="professional_signup"),
    path("professional-verify-otp", ProfessionalVerifyOTPView.as_view(), name="professional_verify_otp"),

    path("forgot-password", ForgotPasswordRequestView.as_view(), name="forgot_password"),
    path("verify-forgot-password-otp", VerifyForgotPasswordOTPView.as_view(), name="verify_forgot_password_otp"),
    path("reset-password", ResetPasswordView.as_view(), name="reset_password"),
]