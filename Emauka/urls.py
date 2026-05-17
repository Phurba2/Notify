from django.urls import path
from .views import EmaukaMailView, EmaukaInappView

urlpatterns = [
    path("emauka/mail", EmaukaMailView.as_view(), name="emauka_mail"),
    path("emauka/inapp", EmaukaInappView.as_view(), name="emauka_inapp"),
]