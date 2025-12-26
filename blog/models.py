from django.db import models
from django.contrib.auth import get_user_model
from cloudinary import CloudinaryImage

User = get_user_model()

class Blog(models.Model):
    text = models.CharField(max_length=140)
    about = models.CharField(max_length = 200, blank=True,)
    banner = models.ImageField(blank=True, null=True, upload_to='banners/')
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    
    def add_collaborator(self, account):
        if account not in self.collaborators:
            self.collaborators.add(account)
            self.save()

    @property
    def banner_url(self):
        if self.banner:
            return self.banner.url
        
        return 'https://res.cloudinary.com/drudyw2gl/image/upload/v1766712403/libro-pasando-paginas_pccza0_c_fill_w_240_h_135_ar_16_9_nqefmh.jpg'
    
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






