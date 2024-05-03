from django import forms
from . models import *

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Оставьте комментарий!'
        }
    ))
