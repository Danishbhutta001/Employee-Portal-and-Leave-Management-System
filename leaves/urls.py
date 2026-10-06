from django.urls import path
from leaves import views

urlpatterns = [
    path("", views.leavelist, name="leavesList"),
    path("add/", views.leaveCreate, name="leaveCreate"),

    path(
        "update/<int:id>/",
        views.leaveUpdate,
        name="leaveUpdate"
    ),

    path(
        "delete/<int:id>/",
        views.leaveDelete,
        name="leaveDelete"
    ),
]