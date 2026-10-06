from django.shortcuts import render,redirect,get_object_or_404
from .models import DepartmentModel
from.forms import DepartmentsForm
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required


@login_required
def departmentList(request):
    search=request.GET.get("search","")
    departments=DepartmentModel.objects.all()
    if search:
        departments=departments.filter(name__icontains=search)

    context = {
        "departments": departments,
        "search": search,
    }
    return render(request,"departments/department_list.html",context)



@login_required
@admin_required
def departmentCreate(request):
    if request.method=="POST":
        form=DepartmentsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("departmentsList")
    else:
        form=DepartmentsForm()

    return render(request,"departments/department_form.html",{"form": form})

@login_required
@admin_required
def departmentDelete(request,id):
    department=get_object_or_404(DepartmentModel,pk=id)
    if request.method=="POST":
        department.delete()
        return redirect("departmentsList")
    return render(
        request,
        "departments/department_confirm_delete.html",
        {"department": department})


@login_required
@admin_required
def departmentUpdate(request,id):
    department=get_object_or_404(DepartmentModel,pk=id)
    if request.method=="POST":
        form=DepartmentsForm(request.POST,instance=department)
        if form.is_valid():
            form.save()
            return redirect("departmentsList")
    else:
        form=DepartmentsForm(instance=department)

    return render(request,"departments/department_form.html",{"form": form})


    



