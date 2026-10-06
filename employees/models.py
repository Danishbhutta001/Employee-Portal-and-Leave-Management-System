from django.db import models
from django.contrib.auth.models import User
from departments.models import DepartmentModel

# Create your models here.

class  EmployeeModel(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    employee_id=models.CharField(max_length=20,unique=True)
    department=models.ForeignKey(DepartmentModel ,on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="employees/", blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.employee_id} - {self.user.username}"
