from django import forms
from .models import DocumentsModel


class DocumentForm(forms.ModelForm):

    class Meta:
        model = DocumentsModel
        fields = ["document_type","file"]