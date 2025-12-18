from django.db import models
from blog.models import EntryComment, CommentResponse, Entry, Blog
from friends.models import FriendRequest
from collaborators.models import CollabRequest
from django.conf import settings


User = settings.AUTH_USER_MODEL


class NotificationType(models.TextChoices):
    COMMENT = 'comment', 'comentario'
    RESPONSE = 'response', 'respuesta'
    ENTRY = 'entry', 'entrada'
    BLOG = 'blog', 'blog'
    FRIEND_REQUEST = 'friend request', 'solicitud de amistad'
    COLLAB_REQUEST = 'collab request', 'solicitud de colaboración'
    

class BaseNotification(models.Model):
    target = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=(models.CASCADE), 
                                related_name='%(class)s_notifications')
    notification_type = models.CharField(max_length=30, choices=NotificationType.choices)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def mark_as_read(self, commit=True):
        self.is_read = True
        if commit:
            self.save(update_fields=['is_read'])


class CommentNotification(BaseNotification):
    creator = models.OneToOneField(EntryComment, on_delete=(models.CASCADE), 
                related_name='notification')
    
    
class ResponseNotification(BaseNotification):
    creator = models.OneToOneField(CommentResponse, on_delete=(models.CASCADE), 
                related_name='notification')
    
    
class FriendRequestNotification(BaseNotification):
    creator = models.OneToOneField(FriendRequest, on_delete=(models.CASCADE),
                related_name='notification')
    
    
class CollabRequestNotification(BaseNotification):
    creator = models.OneToOneField(CollabRequest, on_delete=(models.CASCADE),
                related_name='notification')
    
        
class NewEntryNotification(BaseNotification):
    creator = models.ForeignKey(Entry, on_delete=(models.CASCADE),
                related_name="notification")
    

class NewBlogNotification(BaseNotification):
    creator = models.ForeignKey(Blog, on_delete=(models.CASCADE),
                related_name="notification")
    

    
       
    


