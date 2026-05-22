from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from Elite_freelancer.views import NotifyView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("notify/", NotifyView.as_view(), name="notify"),

    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("", include("Elite_freelancer.urls")),
    path("", include("Emauka.urls")),
]