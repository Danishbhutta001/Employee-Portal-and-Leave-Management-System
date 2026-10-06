from django.shortcuts import render,get_object_or_404,redirect
from .models import EmployeeModel
from .forms import EmployeesForm
from departments.models import DepartmentModel
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required
from django.db.models import Q
from leaves.models import LeaveBalance


# Create your views here.
@login_required
@admin_required
def employeelist(request):
    search=request.GET.get("search")
    department=request.GET.get("department")
    employees=EmployeeModel.objects.all()
    departments=DepartmentModel.objects.all().order_by("name")
    if search:
        employees=employees.filter(Q(user__username__icontains=search)|
                                    Q(department__name__icontains=search))

    if department:
        employees=employees.filter(department_id=department)

    context={
        "employees":employees,
        "department":department,
        "search":search,
        "departments":departments
    }
    return render(request,"employees/employee_list.html",context)

@login_required
@admin_required
def employeeCreate(request):
    if request.method=="POST":
        form= EmployeesForm(request.POST)
        if form.is_valid():
            employee=form.save()
            LeaveBalance.objects.create(employee=employee)

            return redirect("employeesList")
    else:
        form=EmployeesForm()

    return render(request,"employees/employee_form.html",{"form": form})

@login_required
@admin_required
def employeeUpdate(request,id):
    employee=get_object_or_404(EmployeeModel,pk=id)
    if request.method=="POST":
        form=EmployeesForm(request.POST,instance=employee)
        if form.is_valid():
            form.save()
            return redirect("employeesList")
    else:
        form=EmployeesForm(instance=employee)

    return render(request,"employees/employee_form.html",{"form": form})


@login_required
@admin_required
def employeeDelete(request,id):
    employee=get_object_or_404(EmployeeModel,pk=id)
    if request.method=="POST":
        employee.delete()
        return redirect("employeesList")

    return render(request,"employees/employee_confirm_delete.html",{"employee": employee})