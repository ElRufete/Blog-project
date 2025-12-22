from django.db import models
from django.contrib.auth import get_user_model
from cloudinary import CloudinaryImage

User = get_user_model()

class Blog(models.Model):
    text = models.CharField(max_length=140)
    about = models.CharField(max_length = 200, blank=True,)
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    
    def add_collaborator(self, account):
        if account not in self.collaborators:
            self.collaborators.add(account)
            self.save()
    
class Entry(models.Model):
    class Meta():
        verbose_name_plural = 'Entries'

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default= 'Nueva entrada')
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=(models.CASCADE), related_name="collab_entries")
    banner = models.ImageField(upload_to= 'banners', blank=True, null=True)
                                

    def __str__(self):
        return self.title
    
class EntryComment(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class CommentResponse(models.Model):
    comment = models.ForeignKey(EntryComment, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text






