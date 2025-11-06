from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Blog, Entry, EntryComment, CommentResponse

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['text']
        labels = {'text':''}
        

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'text',]
        labels = {'title': 'Título', 'text': '',}
        widgets = {'text': forms.Textarea(attrs={'cols':80, 'rows':16})}

class EntryCommentForm(forms.ModelForm):
    class Meta:
        model = EntryComment
        fields = ['text']
        labels = {'text': ''}

class CommentResponseForm(forms.ModelForm):
    class Meta:
        model = CommentResponse
        fields = ['text']
        labels = {'text': ''}

    
