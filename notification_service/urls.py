from django.contrib import admin
from django.urls import path
from gateway.views import NotifyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notify', NotifyView.as_view()),
]
