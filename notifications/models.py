from django.db import models

# Create your models here.
from django.shortcuts import render
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from leaves.models import LeavesModel


class NotificationsModel(models.Model):

    NOTIFICATION_TYPES = [
    ("LEAVE", "Leave"),
    ("DOCUMENT", "Document"),
    ("SYSTEM", "System"),]
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    leave=models.ForeignKey(LeavesModel,on_delete=models.CASCADE,blank=True,null=True)
    notification_type=models.CharField(max_length=20,choices=NOTIFICATION_TYPES)
    title=models.CharField(max_length=40)
    message=models.TextField()
    is_read=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

