from django import forms
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE

from .models import Blog, Entry, EntryComment, CommentResponse


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['text','about', 'banner']
        labels = {'text':'Título',
                  'about': 'Descripción',
                  'banner': 'Imagen de portada',}
        widgets = {
            'about': forms.Textarea(attrs={'cols':80, 'rows': 3}),
            'text': forms.Textarea(attrs={'cols':50, 'rows': 1}),}
        

class EntryForm(forms.ModelForm):
    text = forms.CharField(
        widget=TinyMCE(
            attrs={'rows': 30, 'cols': 80},
            mce_attrs={
                'upload_imagetab': True,
                'paste_data_images': True,
            }
            )
                           )
    class Meta:
        model = Entry
        fields = ['title', 'banner', 'text',]
        labels = {
            'title': 'Título', 
            'text': '',
            'banner': 'Imagen de portada',
            }
        widgets = { }

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

    
