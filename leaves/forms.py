from django import forms
from .models import LeavesModel


class LeaveForm(forms.ModelForm):

    class Meta:
        model = LeavesModel
        fields = [
            "leave_type",
            "start_date",
            "end_date",
            "reason",
            "medical_certificate"
        ]

        widgets = {
            "start_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
            "end_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
            "reason": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")


class AdminLeaveForm(forms.ModelForm):

    class Meta:
        model = LeavesModel
        fields = "__all__"

        widgets = {
            "start_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
            "end_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
            "reason": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs.setdefault("class", "form-control")

        # Read-only fields

        self.fields["employee"].disabled = True
        self.fields["leave_type"].disabled = True
        self.fields["start_date"].disabled = True
        self.fields["end_date"].disabled = True
        self.fields["reason"].disabled = True
        self.fields["approved_by"].disabled = True
        self.fields["created_at"].disabled = True

        # Only Status is editable
        self.fields["status"].disabled = False