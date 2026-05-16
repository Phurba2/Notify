from django.contrib import admin
from django.urls import path, include
from Elite_freelancer.views import NotifyView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notify', NotifyView.as_view()),
    path("", include("Elite_freelancer.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
