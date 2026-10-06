from django.urls import path
from notifications import views

urlpatterns = [
    path("", views.notificationsList, name="notificationsList"),
    path("<int:notification_id>/",views.notificationRead,name="notificationRead"),
]