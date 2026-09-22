from .models import Notification, ContactMessage


def notification_count(request):

    if request.user.is_authenticated:

        count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()

        return {
            "notification_count": count
        }

    return {
        "notification_count": 0
    }


def contact_message_count(request):
    unread_count = ContactMessage.objects.filter(is_read=False).count()
    return {
        "contact_message_count": unread_count
    }

