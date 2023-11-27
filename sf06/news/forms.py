from django import forms
from .models import * 

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'category', 'header', 'text', ]
        