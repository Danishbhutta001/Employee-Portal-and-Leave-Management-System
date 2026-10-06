from django.db.models.signals import post_save
from leaves.models import LeavesModel
from notifications.models import NotificationsModel
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(post_save, sender=LeavesModel)
def leave_notification(sender, instance, created, **kwargs):

    if created:
        admins=User.objects.filter(groups__name="Admin")

        for admin in admins:
            NotificationsModel.objects.create(
                        user=admin,
                        leave=instance,
                        notification_type="LEAVE",
                        title="New Leave Request",
                        message=f"{instance.employee.user.get_full_name()} has submitted a new leave request."
                    )
            
        return

    if instance.status == "APPROVED":

        NotificationsModel.objects.create(
            user=instance.employee.user,
            leave=instance,
            notification_type="LEAVE",
            title="Leave Approved",
            message="Your leave request has been approved."
        )

    elif instance.status == "REJECTED":

        NotificationsModel.objects.create(
            user=instance.employee.user,
            leave=instance,
            notification_type="LEAVE",
            title="Leave Rejected",
            message="Your leave request has been rejected."
        )