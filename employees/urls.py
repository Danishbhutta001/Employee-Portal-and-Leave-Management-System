from django.urls import path
from employees import views

urlpatterns = [
    path("",views.employeelist,name="employeesList"),
    path("add/",views.employeeCreate,name="employeeCreate"),
    path("delete/<int:id>/",views.employeeDelete,name="employeeDelete"),
    path("update/<int:id>/",views.employeeUpdate,name="employeeUpdate"),



]
