from django.db import models
from blog.models import Blog
from django.conf import settings

User = settings.AUTH_USER_MODEL

class CollabList(models.Model):
    """A list of people who can create entries in blogs from other author"""
    blog = models.OneToOneField(Blog, on_delete=(models.CASCADE), related_name='collaborators')
    collab_list = models.ManyToManyField(User, blank=True, related_name='collaborations')

    def add_collaborator(self, account):
        """Adds a new collaborator"""
        if account not in self.collab_list.all():
            self.collab_list.add(account)

    def remove_collaborator(self,account):
        """Eliminates an account from the collaborators list"""
        if account in self.collab_list.all():
            self.collab_list.remove(account)


class CollabRequest(models.Model):
    """Manages collaboration requests"""
    blog = models.ForeignKey(Blog, on_delete=(models.CASCADE), 
                            related_name='collab_requests')
    sender = models.ForeignKey(User, on_delete=(models.CASCADE), 
                            related_name = "collab_requests_sent")
    receiver = models.ForeignKey(User, on_delete=(models.CASCADE), 
                            related_name = "collab_requests_received")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def accept(self):
        """adds the receiver to blog collaborators and makes request inactive"""
        blog_collabs = CollabList.objects.get(blog=self.blog)
        if blog_collabs:
            blog_collabs.add_collaborator(self.receiver)
        self.is_active = False
        self.save()

    def decline(self):
        """makes request inactive (this action is taken by the receiver)"""
        self.is_active = False
        self.save()
    
    def cancel(self):
        """makes request inactive (this action is taken by the sender)"""
        self.is_active = False
        self.save()

    def renew(self):
        """makes request active again"""
        self.is_active = True
        self.save()