from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import NotificationsModel



@login_required
def notificationsList(request):

    notifications = NotificationsModel.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "notifications/notifications_list.html",
        {
            "notifications": notifications
        }
    )

@login_required
def notificationRead(request,notification_id):
    notification=get_object_or_404(NotificationsModel,id=notification_id)

    if request.user== notification.user:
        notification.is_read=True
        notification.save()
        if notification.leave:
            return redirect(
                "leaveUpdate",
                id=notification.leave.id
            )

    return redirect("notificationsList")

    