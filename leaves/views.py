from django.shortcuts import render,redirect,get_object_or_404
from .models import LeavesModel
from.forms import LeaveForm,AdminLeaveForm
from employees.models import EmployeeModel
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def leavelist(request):
    search=request.GET.get("search")
    if request.user.groups.filter(name="Admin").exists():     
        leaves=LeavesModel.objects.all()
        if search:
            leaves=leaves.filter(employee__user__username__icontains=search)
    else:
        leaves=LeavesModel.objects.filter(employee__user=request.user)
        if search:
            leaves=leaves.filter(employee__user__username__icontains=search)

    status=request.GET.get("status")
    if status:
        leaves=leaves.filter(status__icontains=status)


    return render(request,"leaves/leaves_list.html",{"leaves":leaves})

# Create your views here.
@login_required
def leaveCreate(request):
    if request.method=="POST":
        form=LeaveForm(request.POST)
        if form.is_valid():
           leave=form.save(commit=False)
           leave.employee=EmployeeModel.objects.get(user=request.user)
           leave.save()
           return redirect("leavesList")
    else:
        form=LeaveForm()

    
@login_required
def leaveCreate(request):
    if request.method=="POST":
        form=LeaveForm(request.POST,request.FILES)
        if form.is_valid():
           leave=form.save(commit=False)
           leave.employee=EmployeeModel.objects.get(user=request.user)
           days=(leave.end_date - leave.start_date).days
           if (days>2 and leave.leave_type=="SICK" and not leave.medical_certificate) :
               messages.error(request,"Medical Certficate  require if You Want Leave More then 2 days")
               return render(request,"leaves/leave_form.html",{"form":form})

           if (leave.leave_type=="CASUAL" and days>2):
                messages.error(request,"You can apply for a maximum of 2 Casual Leave days")
                return render(request, "leaves/leave_form.html", {"form": form}) 
           leave.save()
           messages.success(request, "Leave request submitted successfully.")


           return redirect("leavesList")
    else:
        form=LeaveForm()

    
    return render(request,"leaves/leave_form.html",{"form":form})

@login_required
def leaveUpdate(request, id):

    leave = get_object_or_404(LeavesModel, pk=id)

    # Select form based on user role
    if request.user.groups.filter(name="Admin").exists():
        Form = AdminLeaveForm
    else:
        Form = LeaveForm

    if request.method == "POST":

        form = Form(request.POST, instance=leave)

        if form.is_valid():

            leave = form.save(commit=False)

            if request.user.groups.filter(name="Admin").exists():

                if leave.status in ["APPROVED", "REJECTED"]:
                    leave.approved_by = request.user

            leave.save()

            return redirect("leavesList")

    else:

        form = Form(instance=leave)

    return render(
        request,
        "leaves/leave_form.html",
        {
            "form": form
        }
    )


@login_required
def leaveDelete(request,id):
    leave=get_object_or_404(LeavesModel,pk=id)
    if request.method=="POST":
        leave.delete()
        return redirect("leavesList")
    return render(request,"leaves/leave_confirm_delete.html",{"leave":leave})