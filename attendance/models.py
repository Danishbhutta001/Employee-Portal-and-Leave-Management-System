from django.db import models
from employees.models import EmployeeModel
from django.utils import timezone

class AttendanceModel(models.Model):
    status_choice=[
    ("PRESENT", "Present"),
    ("ABSENT", "Absent"),
    ("LATE", "Late"),
    ("HALF_DAY", "Half Day"),
    ]
    employee=models.ForeignKey(EmployeeModel,on_delete=models.CASCADE)
    date=models.DateField(default=timezone.localdate)
    check_in=models.DateTimeField(null=True,blank=True)
    check_out=models.DateTimeField(null= True,blank= True)
    working_hours = models.DecimalField(
    max_digits=5,
    decimal_places=2,
    null=True,
    blank=True
)
    status=models.CharField(max_length= 20,choices=status_choice,default="PRESENT")

    class Meta:
        constraints=[
            models.UniqueConstraint(
                fields=["employee","date"],
                name="employee_attenadce_per_day"
            )
        ]

        ordering=["-date"]