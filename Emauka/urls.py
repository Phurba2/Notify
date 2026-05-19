from django.urls import path
from .views import EmaukaMailView, EmaukaInappView, EmaukaInappListView, EmaukaBroadcastInappView

urlpatterns = [
    path("emauka/mail", EmaukaMailView.as_view(), name="emauka_mail"),
    path("emauka/inapp", EmaukaInappView.as_view(), name="emauka_inapp"),
    path("emauka/inapp-list", EmaukaInappListView.as_view(), name="emauka_inapp_list"),
    path("emauka/inapp-broadcast", EmaukaBroadcastInappView.as_view(), name="emauka_inapp_broadcast"),
]