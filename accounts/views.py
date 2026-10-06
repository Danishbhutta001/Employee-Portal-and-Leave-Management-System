from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def loginViews(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect("dashboard")

    else:
        form = AuthenticationForm()

    return render(
        request,
        "registration/login.html",
        {"form": form}
    )



def LogoutView(request):
    if request.method=="POST":
        logout(request)

        messages.success(request,"Logout Successfully")

        return redirect("login")
    return redirect("employeesList")