from django.urls import path
from accounts import views

urlpatterns = [
    path("",views.loginViews, name="login"),
    path("logout/",views.LogoutView, name="logout")

]
