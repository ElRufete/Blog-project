from django import forms

from .models import Blog, Entry

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

    
