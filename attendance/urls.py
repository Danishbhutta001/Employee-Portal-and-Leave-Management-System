from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.attendanceList,
        name="attendanceList"
    ),

    path(
        "action/",
        views.attendanceAction,
        name="attendanceAction"
    ),

    path(
        "check-in/",
        views.checkIn,
        name="checkIn"
    ),

    path(
        "check-out/",
        views.checkOut,
        name="checkOut"
    ),

]