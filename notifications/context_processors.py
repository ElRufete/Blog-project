from .models import BaseNotification

def unread_notifications_counter(request):
    if request.user.is_authenticated:
        count = BaseNotification.objects.filter(
                    target=request.user,
                    is_read=False,
                    ).count()
         
        return {
                'unread_notifications_counter' : count,
                'unread_notifications_display' : '99+' if count > 99 else count
                }
        
    return {}