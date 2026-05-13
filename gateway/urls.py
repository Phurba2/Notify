from django.urls import path
from .views import (
    NotifyView,
    webhook_receiver,
    ProfessionalSignupView,
    ProfessionalVerifyOTPView,
)

urlpatterns = [
    path("notify", NotifyView.as_view(), name="notify"),
    path("webhook-receiver/", webhook_receiver, name="webhook_receiver"),

    path("professional-signup", ProfessionalSignupView.as_view(), name="professional_signup"),
    path("professional-verify-otp", ProfessionalVerifyOTPView.as_view(), name="professional_verify_otp"),
]