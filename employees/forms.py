from django import forms
from.models import EmployeeModel

class EmployeesForm(forms.ModelForm): 
    class Meta:
        model=EmployeeModel
        fields=["user",
            "employee_id",
            "department",
            "designation",
            "phone",
            "address",
            "date_of_birth",
            "hire_date",
            "salary",
            "profile_picture",
            "status", ]
        

        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "hire_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            # Checkbox
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"

            # File Upload
            elif isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs["class"] = "form-control"

            # Date fields (already have class)
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.setdefault("class", "form-control")

            # All remaining fields
            else:
                field.widget.attrs["class"] = "form-control"