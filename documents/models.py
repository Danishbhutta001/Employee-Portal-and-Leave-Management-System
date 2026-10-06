from django.db import models
from employees.models import EmployeeModel
from django.utils import timezone

# Create your models here.
class DocumentsModel(models.Model):
     DOCUMENT_TYPE_CHOICES = [
        ("RESUME", "Resume"),
        ("CNIC", "CNIC"),
        ("PASSPORT", "Passport"),
        ("DEGREE", "Degree"),
        ("EXPERIENCE_LETTER", "Experience Letter")]
     employee = models.ForeignKey(EmployeeModel,on_delete=models.CASCADE)
     document_type = models.CharField( max_length=30,choices=DOCUMENT_TYPE_CHOICES)
     file = models.FileField(upload_to="documents/")
     uploaded_at = models.DateTimeField(default=timezone.now)


     def __str__(self):
      return f"{self.employee.user.username} - {self.document_type}"


    