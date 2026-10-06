from django.db import models
from django.utils import timezone

# Create your models here.

class DepartmentModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField( max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

