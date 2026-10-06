from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from departments.models import DepartmentModel
from employees.models import EmployeeModel
from documents.models import DocumentsModel
from leaves.models import LeavesModel


@login_required
def dashboardView(request):

    if request.user.groups.filter(name="Admin").exists():

        context = {
            "total_employees": EmployeeModel.objects.count(),
            "total_departments": DepartmentModel.objects.count(),
            "total_leaves": LeavesModel.objects.count(),
            "pending_leaves": LeavesModel.objects.filter(status="PENDING").count(),
            "approved_leaves": LeavesModel.objects.filter(status="APPROVED").count(),
            "rejected_leaves": LeavesModel.objects.filter(status="REJECTED").count(),
            "total_documents": DocumentsModel.objects.count(),

            "recent_employees": EmployeeModel.objects.order_by("-id")[:5],
            "recent_leaves": LeavesModel.objects.order_by("-created_at")[:5],
            "recent_documents": DocumentsModel.objects.order_by("-uploaded_at")[:5],
        }
        return render(request, "dashboard/admin_dashboard.html", context)

    else:

        context = {
            "my_leaves": LeavesModel.objects.filter(employee__user=request.user).count(),
            "pending_leaves": LeavesModel.objects.filter(
                employee__user=request.user,
                status="PENDING"
            ).count(),
            "approved_leaves": LeavesModel.objects.filter(
                employee__user=request.user,
                status="APPROVED"
            ).count(),
            "rejected_leaves": LeavesModel.objects.filter(
                employee__user=request.user,
                status="REJECTED"
            ).count(),
            "my_documents": DocumentsModel.objects.filter(
                employee__user=request.user
            ).count(),

            "recent_leaves": LeavesModel.objects.filter(
                employee__user=request.user
            ).order_by("-created_at")[:5],

            "recent_documents": DocumentsModel.objects.filter(
                employee__user=request.user
            ).order_by("-uploaded_at")[:5],
        }

        return render(request, "dashboard/employee_dashboard.html", context)