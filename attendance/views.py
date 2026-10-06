from django.shortcuts import render, redirect
from .models import AttendanceModel
from employees.models import EmployeeModel
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages


@login_required
def attendanceList(request):

    if request.user.groups.filter(name="Admin").exists():

        attendances = AttendanceModel.objects.all()

    else:

        employee = EmployeeModel.objects.get(
            user=request.user
        )

        attendances = AttendanceModel.objects.filter(
            employee=employee
        )

    return render(
        request,
        "attendance/attendance_list.html",
        {
            "attendances": attendances
        }
    )


@login_required
def attendanceAction(request):

    # Admin cannot perform personal attendance
    if request.user.groups.filter(name="Admin").exists():

        messages.error(
            request,
            "Admin users cannot check in or check out."
        )

        return redirect("attendanceList")

    employee = EmployeeModel.objects.get(
        user=request.user
    )

    today = timezone.localdate()

    attendance, created = AttendanceModel.objects.get_or_create(
        employee=employee,
        date=today
    )

    return render(
        request,
        "attendance/attendance_action.html",
        {
            "attendance": attendance
        }
    )


@login_required
def checkIn(request):

    if request.user.groups.filter(name="Admin").exists():

        messages.error(
            request,
            "Admin users cannot check in."
        )

        return redirect("attendanceAction")

    employee = EmployeeModel.objects.get(
        user=request.user
    )

    today = timezone.localdate()

    attendance, created = AttendanceModel.objects.get_or_create(
        employee=employee,
        date=today
    )

    if attendance.check_in:

        messages.warning(
            request,
            "You have already checked in today."
        )

        return redirect("attendanceAction")

    # DateTimeField → use timezone.now()
    attendance.check_in = timezone.now()

    # Must match your model choice
    attendance.status = "PRESENT"

    attendance.save()

    messages.success(
        request,
        "Check-in successful."
    )

    return redirect("attendanceAction")

@login_required
def checkOut(request):

    if request.user.groups.filter(name="Admin").exists():

        messages.error(
            request,
            "Admin users cannot check out."
        )

        return redirect("attendanceAction")

    employee = EmployeeModel.objects.get(
        user=request.user
    )

    today = timezone.localdate()

    try:

        attendance = AttendanceModel.objects.get(
            employee=employee,
            date=today
        )

    except AttendanceModel.DoesNotExist:

        messages.error(
            request,
            "You must check in before checking out."
        )

        return redirect("attendanceAction")

    if not attendance.check_in:

        messages.error(
            request,
            "You must check in before checking out."
        )

        return redirect("attendanceAction")

    if attendance.check_out:

        messages.warning(
            request,
            "You have already checked out today."
        )

        return redirect("attendanceAction")

    # Checkout
    attendance.check_out = timezone.now()

    # Calculate working time
    working_time = attendance.check_out - attendance.check_in

    total_minutes = round(
        working_time.total_seconds() / 60
    )

    # Store decimal hours in database
    attendance.working_hours = round(
        total_minutes / 60,
        2
    )

    attendance.save()

    # Message format
    hours = total_minutes // 60
    minutes = total_minutes % 60

    if hours > 0 and minutes > 0:

        working_display = (
            f"{hours} hour{'s' if hours != 1 else ''} "
            f"{minutes} minute{'s' if minutes != 1 else ''}"
        )

    elif hours > 0:

        working_display = (
            f"{hours} hour{'s' if hours != 1 else ''}"
        )

    else:

        working_display = (
            f"{minutes} minute{'s' if minutes != 1 else ''}"
        )

    messages.success(
        request,
        f"Check-out successful. Working time: {working_display}."
    )

    return redirect("attendanceAction")