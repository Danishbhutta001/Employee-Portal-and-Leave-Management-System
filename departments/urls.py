from django.urls import path
from departments import views


urlpatterns = [
    path("",views.departmentList,name="departmentsList"),
    path("add/",views.departmentCreate,name="departmentCreate"),
    path("edit/<int:id>/",views.departmentUpdate,name="departmentUpdate"),
    path("delete/<int:id>/",views.departmentDelete,name="departmentDelete"),



]
