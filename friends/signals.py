from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FriendsList
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_friends_list(sender, instance, created, **kwargs):
    if created:
        FriendsList.objects.create(user=instance)
