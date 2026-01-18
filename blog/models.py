from django.db import models
from django.contrib.auth import get_user_model

from cloudinary import CloudinaryImage
from cloudinary.models import CloudinaryField



User = get_user_model()

class Blog(models.Model):
    text = models.CharField(max_length=140)
    about = models.CharField(max_length = 200, blank=True,)
    banner = CloudinaryField('banner', blank=True, null=True, transformation=[
            {
            'width': 2000,
            'height': 2000,
            'crop': 'limit',
            'quality': 'auto',
            }
        ]
    )
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    
    def add_collaborator(self, account):
        if account not in self.collaborators:
            self.collaborators.add(account)
            self.save()

    def banner_url(self):

        public_id = self.banner.public_id if self.banner else 'libro-pasando-paginas_pccza0_c_fill_w_240_h_135_ar_16_9_nqefmh'
        return CloudinaryImage(public_id).build_url(
            width=288,
            aspect_ratio='16:9', 
            crop='fill',
            gravity='auto', 
            fetch_format='auto',
            quality='auto',
            )
    
        
    
class Entry(models.Model):
    class Meta():
        verbose_name_plural = 'Entries'

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=(models.CASCADE), related_name="collab_entries")
    banner = CloudinaryField('banner', blank=True, null=True, transformation=[
            {
            'width': 2000,
            'height': 2000,
            'crop': 'limit',
            'quality': 'auto',
            }
        ]
    )
                                
    def banner_card_url(self):

        public_id = self.banner.public_id
        return CloudinaryImage(public_id).build_url(
            width=288,
            aspect_ratio='16:9', 
            crop='fill',
            gravity='auto', 
            fetch_format='auto',
            quality='auto',
            )
    
    
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






