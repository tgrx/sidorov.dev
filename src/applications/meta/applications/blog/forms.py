from django import forms

from applications.meta.applications.blog.models import Comment
from project.utils.xmodels import a


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        widgets = {
            a(Comment.author): forms.HiddenInput,
            a(Comment.post): forms.HiddenInput,
        }
        fields = [a(_f) for _f in (Comment.author, Comment.message, Comment.post,)]
