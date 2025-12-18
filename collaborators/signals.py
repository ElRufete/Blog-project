from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CollabList
from blog.models import Blog


@receiver(post_save, sender=Blog)
def create_collab_list(sender, instance, created, **kwargs):
    if created:
        CollabList.objects.get_or_create(blog=instance)
