from django.shortcuts import render,redirect,get_object_or_404
from .models import DocumentsModel
from.forms import DocumentForm
from employees.models import EmployeeModel
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def documentlist(request):

    search = request.GET.get("search", "")
    document_type = request.GET.get("document_type", "")

    if request.user.groups.filter(name="Admin").exists():
        documents = DocumentsModel.objects.all()
    else:
        documents = DocumentsModel.objects.filter(employee__user=request.user)

    # Search
    if search:
        documents = documents.filter(
            employee__user__username__icontains=search
        )

    # Document Type Filter
    if document_type:
        documents = documents.filter(
            document_type=document_type
        )

    context = {
        "documents": documents,
        "search": search,
        "document_type": document_type,
    }

    return render(request, "documents/documents_list.html", context)

# Create your views here.
@login_required

def documentCreate(request):
    if request.method=="POST":
        form=DocumentForm(request.POST,request.FILES)
        if form.is_valid():
            document=form.save(commit=False)
            document.employee=EmployeeModel.objects.get(user=request.user)
            document.save()

            return redirect("documentsList")
    else:
        form=DocumentForm()
    return render(request,"documents/document_form.html",{"form":form})

@login_required
def documentUpdate(request,id):
    document=get_object_or_404(DocumentsModel,pk=id)
    if request.method=="POST":
        form=DocumentForm(request.POST,request.FILES,instance=document)
        if form.is_valid():
            form.save()
            return redirect("documentsList")
    else:
        form=DocumentForm(instance=document)
    return render(request,"documents/document_form.html",{"form":form})

@login_required
def documentDelete(request,id):
    document=get_object_or_404(DocumentsModel,pk=id)
    if request.method=="POST":
        document.delete()
        return redirect("documentsList")
    return render(request,"documents/document_confirm_delete.html",{"document":document})