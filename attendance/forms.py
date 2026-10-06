from django import forms
from .models import AttendanceModel

class AttendanceForm(forms.ModelForm):
     class Meta:
        model=AttendanceModel
        fields="__all__"