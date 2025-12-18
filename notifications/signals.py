from django.db.models.signals import post_save
from django.dispatch import receiver
from blog.models import EntryComment, CommentResponse, Blog, Entry
from friends.models import FriendRequest
from collaborators.models import CollabRequest
from .models import (CommentNotification, NewEntryNotification, 
                     NotificationType, ResponseNotification, NewBlogNotification, 
                     FriendRequestNotification, CollabRequestNotification)
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

@receiver(post_save, sender=EntryComment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        CommentNotification.objects.create(creator=instance, 
                                           target=instance.entry.author,
                                           notification_type = NotificationType.COMMENT)
        
        
@receiver(post_save, sender=CommentResponse)
def create_response_notification(sender, instance, created, **kwargs):
    if created:
        ResponseNotification.objects.create(creator=instance, 
                                           target=instance.comment.author,
                                           notification_type = NotificationType.RESPONSE)
        
        
@receiver(post_save, sender=FriendRequest)
def sync_friend_request_notification(sender, instance, created, **kwargs):
    notification = getattr(instance, 'notification', None)

    if created:
        FriendRequestNotification.objects.create(creator=instance, 
                                           target=instance.receiver,
                                           notification_type = NotificationType.FRIEND_REQUEST)
    elif notification:
        if instance.is_active:
            notification.is_read = False
            notification.timestamp = timezone.now()

        else:
            notification.is_read = True
    
        notification.save(update_fields=['is_read', 'timestamp'])


@receiver(post_save, sender=CollabRequest)
def create_collab_request_notification(sender, instance, created, **kwargs):
    notification = getattr(instance, 'notification', None)
    if created:
        CollabRequestNotification.objects.create(creator=instance, 
                                           target=instance.receiver,
                                           notification_type = NotificationType.COLLAB_REQUEST)
    elif notification:
        if instance.is_active:
            notification.is_read = False
            notification.timestamp = timezone.now()

        else:
            notification.is_read = True
    
        notification.save(update_fields=['is_read', 'timestamp'])
        

@receiver(post_save, sender=Entry)
def create_new_entry_notification(sender, instance, created, **kwargs):
    if created:
        for friend in instance.author.friends_list.friends.all():
            NewEntryNotification.objects.create(
                        creator = instance,
                        target = friend,
                        notification_type = NotificationType.ENTRY)
                    

@receiver(post_save, sender=Blog)
def create_new_blog_notification(sender, instance, created, **kwargs):
    if created:
        for friend in instance.author.friends_list.friends.all():
            NewBlogNotification.objects.create(
                        creator = instance,
                        target = friend,
                        notification_type = NotificationType.BLOG)
        



        




