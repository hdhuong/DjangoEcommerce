from django.db.models import fields
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Comment


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class CommentForm(forms.ModelForm):
    def __init__(self, *args , **kwargs):
        self.author = kwargs.pop('author',None)
        self.product = kwargs.pop('product',None)
        super().__init__(*args, **kwargs)
    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.author = self.author
        comment.product = self.product
        comment.save()
    class Meta:
        model = Comment
        fields = ['body']

