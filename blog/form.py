from unicodedata import category
from xml.dom.minidom import Attr
from django import forms
from django.forms import ModelForm
from .models import Comment, Post, Category

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        labels = {"username": "Nombre:", "comment": "Comentario:"}
        exclude = ('post',)


class AddPostForm(ModelForm):
    author = forms.CharField(max_length=50, 
                            widget=forms.TextInput(attrs={'class': 'add_post_options'}), required=True,
                            label="Autor (tu nombre):")                       
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label="Escoje la(s) categoría(s) a la(s) que pertenezca tu post:"
    )

    class Meta:
        model = Post
        fields = ("title", "excerpt", "image", "content", "category")
        widgets = {
            'title': forms.TextInput(attrs= {'class': 'add_post_options'}),
            'excerpt': forms.Textarea(attrs= {'class': 'add_post_options', 'rows': 10}),
            'content': forms.Textarea(attrs= {'class': 'add_post_options', 'rows': 20}),
            "category": forms.SelectMultiple(attrs= {'class': 'add_post_options'})
            }
        labels = {"title": "Título del post:", "excerpt": "Premisa:", "content": "Contenido", 
        "image": "Imagen para el post", "category": "Categoría(s):"}