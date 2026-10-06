from django import forms
from .models import DepartmentModel


class DepartmentsForm(forms.ModelForm):
    class Meta:
        model = DepartmentModel
        fields = ["name","description"]
