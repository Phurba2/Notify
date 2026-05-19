from django.urls import path
from .views import EmaukaMailView, EmaukaInappView, EmaukaInappListView

urlpatterns = [
    path("emauka/mail", EmaukaMailView.as_view(), name="emauka_mail"),
    path("emauka/inapp", EmaukaInappView.as_view(), name="emauka_inapp"),
    path("emauka/inapp-list", EmaukaInappListView.as_view(), name="emauka_inapp_list"),
]