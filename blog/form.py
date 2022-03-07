from django.forms import ModelForm
from .models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        labels = {"username": "Nombre:", "comment": "Comentario:"}
        exclude = ('post',)