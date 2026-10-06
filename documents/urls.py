from django.urls import path
from documents import views

urlpatterns = [
    path("",views.documentlist,name="documentsList"),
    path("add/",views.documentCreate,name="documentCreate"),
    path("update/<int:id>/",views.documentUpdate,name="documentUpdate"),
    path("delete/<int:id>/",views.documentDelete,name="documentDelete")



]
