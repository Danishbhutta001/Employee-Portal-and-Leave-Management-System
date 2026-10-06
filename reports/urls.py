from django.urls import path
from . import views

urlpatterns = [
    path("", views.reportsDashboard, name="reportsDashboard"),
    path("leaves/", views.leavesReport, name="leavesReport"),
    path("attendance/", views.attendanceReport, name="attendanceReport"),
    path("employee/", views.employeereport, name="employeeReport"),
    path("employees/export/pdf/",views.employeeExportPdf,name="employeeExportPDF"),
    path("leaves/export/pdf/",views.leaveExportPdf,name="leaveExportPDF"),
    path(
    "attendance/export/pdf/",views.attendanceExportPdf,name="attendanceExportPDF")
]