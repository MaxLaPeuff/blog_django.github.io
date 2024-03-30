from django import forms
from .models import Comment
from django.forms import fields

class BlogForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=[
          
            'body'
        ]