from django import forms
from . models import *

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Оставьте комментарий!',
            'rows': 3,
            'style': 'background: radial-gradient(circle at 24.1% 68.8%,rgb(10, 10, 10) 0%,  rgb(50, 50, 50) 99.4%); color: grey;'
        }
    ))