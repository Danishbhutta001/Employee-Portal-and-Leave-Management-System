from django.shortcuts import render,redirect
from django.http import HttpResponse
from reportlab.pdfgen  import canvas
from reportlab.lib.pagesizes import landscape, letter
from leaves.models import LeavesModel
from attendance.models import AttendanceModel
from employees.models import EmployeeModel
from django.contrib.auth.decorators import login_required
from departments.models import DepartmentModel

# Create your views here.

@login_required
def reportsDashboard(request):

    if not request.user.groups.filter(name="Admin").exists():
        return redirect("dashboard")

    return render(
        request,
        "reports/reports_dashboard.html"
    )


@login_required
def leavesReport(request):
    if request.user.groups.filter(name="Admin").exists():
        leaves=LeavesModel.objects.all()
        pending_leaves = LeavesModel.objects.filter(status="PENDING").count()
        approved_leaves = LeavesModel.objects.filter(status="APPROVED").count()
        rejected_leaves = LeavesModel.objects.filter(status="REJECTED").count()


        

        employees=EmployeeModel.objects.all()

        leave_type = request.GET.get("leave_type")

        employee=request.GET.get("employee")

        status = request.GET.get("status")    
        if employee:
            leaves=leaves.filter(employee_id=employee)
        if leave_type:
            leaves = leaves.filter(leave_type=leave_type)
        if status:
            leaves = leaves.filter(status=status )
    
        return render(request,"reports/leave_report.html",{"leaves":leaves,
                                                           "employees":employees,
                                                           "pending_leaves":pending_leaves,
                                                           "approved_leaves":approved_leaves,
                                                           "rejected_leaves":rejected_leaves})




@login_required
def  attendanceReport(request):
    if request.user.groups.filter(name="Admin").exists():
        attendaces=AttendanceModel.objects.all()
        employees = EmployeeModel.objects.all()
        employee = request.GET.get("employee")
        status = request.GET.get("status")
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        if employee:
            attendaces = attendaces.filter(employee_id=employee)

        if status:
            attendaces = attendaces.filter(status=status)

        if start_date:
            attendaces = attendaces.filter(date__gte=start_date)

        if end_date:
            attendaces = attendaces.filter(date__lte=end_date)
        
        return render(request,"reports/attendace_report.html",{"attendances": attendaces,
                                                                "employees": employees}
)

@login_required
def employeereport(request):
    if request.user.groups.filter(name="Admin").exists():
        employees=EmployeeModel.objects.all()
        departments=DepartmentModel.objects.all()
        employee=request.GET.get("employee")
        department=request.GET.get("department")
        status=request.GET.get("status")
        hire_date=request.GET.get("hire_date")

        if employee:
            employees = employees.filter(id=employee)

        if department:
            employees = employees.filter(department_id=department)

        if status == "ACTIVE":
            employees = employees.filter(status=True)

        elif status == "INACTIVE":
            employees = employees.filter(status=False)
        if hire_date:
            employees = employees.filter(hire_date=hire_date)

            #summary
        total_employees = EmployeeModel.objects.count()

        active_employees = EmployeeModel.objects.filter(
            status=True
        ).count()

        inactive_employees = EmployeeModel.objects.filter(
            status=False
        ).count()

        total_departments = DepartmentModel.objects.count()

        return render(
            request,"reports/employee_report.html",
            {"employees": employees,
            "departments": departments,            
            "total_employees": total_employees,
            "active_employees": active_employees,
            "inactive_employees": inactive_employees,
            "total_departments": total_departments,}
        )



@login_required
def employeeExportPdf(request):
    if not request.user.groups.filter(name="Admin").exists():
        return  redirect("dashboard")
    employees=EmployeeModel.objects.all()

    department=request.GET.get("department")
    status=request.GET.get("status")
    hire_date=request.GET.get("hire_date")

    if department:
        employees=employees.filter(department_id=department)
    if status=="ACTIVE":
        employees=employees.filter(status=True)
    elif status=="INACTIVE":
        employees=employees.filter(status=False)
    if hire_date:
        employees=employees.filter(hire_date=hire_date)
        



    response=HttpResponse(content_type="application/pdf")

    response["Content-Disposition"] = (
        'attachment; filename="employee_report.pdf"')

    pdf=canvas.Canvas(response)

    pdf.setTitle("Employee Report")

    pdf.setFont("Helvetica-Bold",18)

    pdf.drawString(50, 800,"Employee Report")

    pdf.setFont(
        "Helvetica-Bold",
        10
    )

    y = 760

    pdf.drawString(50, y, "Employee ID")
    pdf.drawString(130, y, "Name")
    pdf.drawString(250, y, "Department")
    pdf.drawString(350, y, "Designation")
    pdf.drawString(470, y, "Hire Date")
    pdf.drawString(540, y, "Status")

    pdf.setFont(
        "Helvetica",
        9
    )

    y -= 25

    for employee in employees:

        pdf.drawString(
            50,
            y,
            str(employee.employee_id)
        )

        pdf.drawString(
            130,
            y,
            employee.user.get_full_name()
        )

        pdf.drawString(
            250,
            y,
            employee.department.name
        )

        pdf.drawString(
            350,
            y,
            employee.designation
        )

        pdf.drawString(
            470,
            y,
            str(employee.hire_date)
        )

        if employee.status:
            status = "Active"
        else:
            status = "Inactive"

        pdf.drawString(
            540,
            y,
            status
        )

        # Move down for next employee
        y -= 20

        # New page
        if y < 50:

            pdf.showPage()

            pdf.setFont(
                "Helvetica",
                9
            )

            y = 800

    # Finish PDF
    pdf.save()

    return response


@login_required
def leaveExportPdf(request):

    if not request.user.groups.filter(name="Admin").exists():
        return redirect("dashboard")

    leaves = LeavesModel.objects.all()

    employee_id = request.GET.get("employee")
    leave_type = request.GET.get("leave_type")
    status = request.GET.get("status")

    if employee_id:
        leaves = leaves.filter(employee_id=employee_id)

    if leave_type:
        leaves = leaves.filter(leave_type=leave_type)

    if status:
        leaves = leaves.filter(status=status)

    response = HttpResponse(content_type="application/pdf")

    response["Content-Disposition"] = (
        'attachment; filename="leave_report.pdf"'
    )

    pdf = canvas.Canvas(response, pagesize=landscape(letter))

    pdf.setTitle("Leave Report")

    # Title
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(420, 560, "LEAVE REPORT")

    pdf.setFont("Helvetica", 11)
    pdf.drawCentredString(
        420,
        542,
        "Employee Management Portal"
    )

    # Employee details
    if employee_id and leaves.exists():

        employee = leaves.first().employee

        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(40, 505, "EMPLOYEE INFORMATION")

        pdf.setFont("Helvetica", 10)

        pdf.drawString(
            40, 480,
            f"Employee ID: {employee.employee_id}"
        )

        pdf.drawString(
            300, 480,
            f"Employee Name: {employee.user.get_full_name()}"
        )

        pdf.drawString(
            40, 460,
            f"Department: {employee.department.name}"
        )

        pdf.drawString(
            300, 460,
            f"Designation: {employee.designation}"
        )

        pdf.drawString(
            40, 440,
            f"Email: {employee.user.email}"
        )

        pdf.drawString(
            300, 440,
            f"Phone: {employee.phone}"
        )

        pdf.drawString(
            40, 420,
            f"Hire Date: {employee.hire_date}"
        )

        employee_status = "Active" if employee.status else "Inactive"

        pdf.drawString(
            300, 420,
            f"Employment Status: {employee_status}"
        )

        y = 380

    else:

        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(40, 505, "LEAVE SUMMARY")

        y = 470

    
    total = leaves.count()
    pending = leaves.filter(status="PENDING").count()
    approved = leaves.filter(status="APPROVED").count()
    rejected = leaves.filter(status="REJECTED").count()

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(40, y, "LEAVE SUMMARY")

    y -= 25

    pdf.setFont("Helvetica", 10)

    pdf.drawString(40, y, f"Total Leaves: {total}")
    pdf.drawString(180, y, f"Pending: {pending}")
    pdf.drawString(300, y, f"Approved: {approved}")
    pdf.drawString(420, y, f"Rejected: {rejected}")

    # Leave records
    y -= 45

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(40, y, "LEAVE RECORDS")

    y -= 25

    pdf.setFont("Helvetica-Bold", 9)

    pdf.drawString(40, y, "Leave Type")
    pdf.drawString(170, y, "Start Date")
    pdf.drawString(270, y, "End Date")
    pdf.drawString(370, y, "Status")
    pdf.drawString(470, y, "Approved By")

    pdf.line(40, y - 5, 720, y - 5)

    y -= 25

    pdf.setFont("Helvetica", 9)

    for leave in leaves:

        approved_by = "-"

        if leave.approved_by:
            approved_by = leave.approved_by.get_full_name()

            if not approved_by:
                approved_by = leave.approved_by.username

        pdf.drawString(
            40,
            y,
            leave.get_leave_type_display()
        )

        pdf.drawString(
            170,
            y,
            str(leave.start_date)
        )

        pdf.drawString(
            270,
            y,
            str(leave.end_date)
        )

        pdf.drawString(
            370,
            y,
            leave.status
        )

        pdf.drawString(
            470,
            y,
            approved_by[:20]
        )

        y -= 20

        if y < 40:

            pdf.showPage()

            pdf.setFont("Helvetica", 9)

            y = 550

    pdf.save()

    return response

@login_required
def attendanceExportPdf(request):

    if not request.user.groups.filter(name="Admin").exists():
        return redirect("dashboard")

    attendances = AttendanceModel.objects.all()

    employee_id = request.GET.get("employee")
    status = request.GET.get("status")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if employee_id:
        attendances = attendances.filter(
            employee_id=employee_id
        )

    if status:
        attendances = attendances.filter(
            status=status
        )

    if start_date:
        attendances = attendances.filter(
            date__gte=start_date
        )

    if end_date:
        attendances = attendances.filter(
            date__lte=end_date
        )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        'attachment; filename="attendance_report.pdf"'
    )

    pdf = canvas.Canvas(
        response,
        pagesize=landscape(letter)
    )

    pdf.setTitle("Attendance Report")

    pdf.setFont("Helvetica-Bold", 20)

    pdf.drawCentredString(
        420,
        560,
        "ATTENDANCE REPORT"
    )

    pdf.setFont("Helvetica", 11)

    pdf.drawCentredString(
        420,
        542,
        "Employee Management Portal"
    )

    y = 505

    if employee_id:

        employee = EmployeeModel.objects.get(
            id=employee_id
        )

        pdf.setFont("Helvetica-Bold", 13)

        pdf.drawString(
            40,
            y,
            "EMPLOYEE INFORMATION"
        )

        y -= 25

        pdf.setFont("Helvetica", 10)

        name = employee.user.get_full_name()

        if not name:
            name = employee.user.username

        employee_status = (
            "Active"
            if employee.status
            else "Inactive"
        )

        pdf.drawString(
            40,
            y,
            f"Employee ID: {employee.employee_id}"
        )

        pdf.drawString(
            300,
            y,
            f"Employee Name: {name}"
        )

        y -= 20

        pdf.drawString(
            40,
            y,
            f"Department: {employee.department.name}"
        )

        pdf.drawString(
            300,
            y,
            f"Designation: {employee.designation}"
        )

        y -= 20

        pdf.drawString(
            40,
            y,
            f"Email: {employee.user.email}"
        )

        pdf.drawString(
            300,
            y,
            f"Phone: {employee.phone}"
        )

        y -= 20

        pdf.drawString(
            40,
            y,
            f"Hire Date: {employee.hire_date}"
        )

        pdf.drawString(
            300,
            y,
            f"Employment Status: {employee_status}"
        )

        y -= 40

    total = attendances.count()

    present = attendances.filter(
        status="PRESENT"
    ).count()

    absent = attendances.filter(
        status="ABSENT"
    ).count()

    late = attendances.filter(
        status="LATE"
    ).count()

    pdf.setFont("Helvetica-Bold", 13)

    pdf.drawString(
        40,
        y,
        "ATTENDANCE SUMMARY"
    )

    y -= 25

    pdf.setFont("Helvetica", 10)

    pdf.drawString(
        40,
        y,
        f"Total Records: {total}"
    )

    pdf.drawString(
        180,
        y,
        f"Present: {present}"
    )

    pdf.drawString(
        300,
        y,
        f"Absent: {absent}"
    )

    pdf.drawString(
        420,
        y,
        f"Late: {late}"
    )

    y -= 45

    pdf.setFont("Helvetica-Bold", 13)

    pdf.drawString(
        40,
        y,
        "ATTENDANCE RECORDS"
    )

    y -= 25

    pdf.setFont("Helvetica-Bold", 9)

    pdf.drawString(40, y, "Date")
    pdf.drawString(150, y, "Check In")
    pdf.drawString(240, y, "Check Out")
    pdf.drawString(340, y, "Working Hours")
    pdf.drawString(470, y, "Status")

    pdf.line(
        40,
        y - 5,
        720,
        y - 5
    )

    y -= 25

    pdf.setFont("Helvetica", 9)

    for attendance in attendances:

        check_in = (
            attendance.check_in.strftime("%I:%M %p")
            if attendance.check_in
            else "-"
        )

        check_out = (
            attendance.check_out.strftime("%I:%M %p")
            if attendance.check_out
            else "-"
        )

        working_hours = (
            str(attendance.working_hours)
            if attendance.working_hours
            else "-"
        )

        pdf.drawString(
            40,
            y,
            attendance.date.strftime("%d %b %Y")
        )

        pdf.drawString(
            150,
            y,
            check_in
        )

        pdf.drawString(
            240,
            y,
            check_out
        )

        pdf.drawString(
            340,
            y,
            working_hours
        )

        pdf.drawString(
            470,
            y,
            str(attendance.status)
        )

        y -= 20

        if y < 40:

            pdf.showPage()

            pdf.setFont(
                "Helvetica",
                9
            )

            y = 550

    pdf.save()

    return response