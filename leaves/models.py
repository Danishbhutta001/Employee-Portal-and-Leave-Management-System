from django.db import models
from employees.models import EmployeeModel
from django.contrib.auth.models import User
from django.utils import timezone


class LeavesModel(models.Model):
    Status_Choice=[
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ]

    Leave_Type_Choice=[
        ("CASUAL", "Casual Leave"),
        ("SICK", "Sick Leave"),
        ("ANNUAL", "Annual Leave"),]
    id=models.AutoField(primary_key=True)
    employee=models.ForeignKey(EmployeeModel,on_delete=models.CASCADE)
    leave_type=models.CharField(max_length=50,choices=Leave_Type_Choice)
    start_date=models.DateField()
    end_date=models.DateField()
    reason=models.TextField()
    status = models.CharField(max_length=20,choices=Status_Choice,default="PENDING")
    approved_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    medical_certificate=models.FileField(upload_to="medical_certificates/",blank=True,null=True)


    def __str__(self):
        return f"{self.employee.user.username} - {self.leave_type}"
        \

class LeaveBalance(models.Model):
    employee=models.OneToOneField(EmployeeModel,on_delete=models.CASCADE)
    casual_allowed=models.PositiveIntegerField(default=12)
    casual_used=models.PositiveIntegerField(default=0)
    casual_remaining=models.PositiveIntegerField(default=12)
    sick_allowed=models.PositiveIntegerField(default=12)
    sick_used=models.PositiveIntegerField(default=0)
    sick_remaining=models.PositiveIntegerField(default=12)
    anual_allowed=models.PositiveIntegerField(default=12)
    anual_used=models.PositiveIntegerField(default=0)
    anual_remaining=models.PositiveIntegerField(default=12)


