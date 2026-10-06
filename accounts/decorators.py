from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):

    def wrapper(request, *args, **kwargs):

        if request.user.groups.filter(name="Admin").exists():
            return view_func(request, *args, **kwargs)

        messages.error(request, "You are not authorized to access this page.")

        return redirect("login")

    return wrapper