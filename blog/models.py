from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    text = models.CharField(max_length=140)
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
    
class Entry(models.Model):
    class Meta():
        verbose_name_plural = 'Entries'

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default= 'Nueva entrada')
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(blank = True)

    def __str__(self):
        return self.title
    



