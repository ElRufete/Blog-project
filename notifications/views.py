from django.shortcuts import render
from .models import BaseNotification

def activity(request):
    notifications = BaseNotification.objects.filter(
        target = request.user
    ).order_by('-timestamp')
    unread_notifications = BaseNotification.objects.filter(
        target = request.user,
        is_read = False
    )
    unread_notifications.update(is_read=True)
    context = {
        'notifications' : notifications, 
    }
    return render(request, 'notifications/activity.html', context)

