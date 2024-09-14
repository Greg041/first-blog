# Django imports
from django import forms
from django.utils.translation import gettext_lazy as _
# Local imports
from .models import Comment, Post, Category
# Third party apps imports
from cloudinary.forms import CloudinaryFileField
from tinymce.widgets import TinyMCE


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        labels = {"username": "Nombre:", "comment": "Comentario:"}
        exclude = ("post",)
        
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AddPostForm(forms.ModelForm):                
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label="Escoje la(s) categoría(s) a la(s) que pertenezca tu post:"
    )
    image = CloudinaryFileField(label="Imagen banner para el post")

    class Meta:
        model = Post
        fields = ("title", "excerpt", "image", "content", "category")
        widgets = {
            "title": forms.TextInput(attrs={"class": "add_post_options"}),
            "excerpt": TinyMCE(attrs={"class": "add_post_options", "rows": 10}),
            "content": TinyMCE(attrs={"class": "add_post_options", "rows": 20}),
        }
        labels = {"title": "Título del post:", "excerpt": "Premisa:", "content": "Contenido:"}

    def __init__(self, *args, **kwargs):
        super(AddPostForm, self).__init__(*args, **kwargs)
        self.fields["image"].options = {
            "tags": "image",
            "format": "png",
        }
        # We add bootstrap classes to form fields
        for visible in self.visible_fields():
            if visible.name != "category":
                visible.field.widget.attrs["class"] = " form-control"
                if visible.errors:
                    visible.field.widget.attrs["class"] += " is-invalid"
        self.fields["title"].widget.attrs["class"] += " w-100 w-sm-50"
        self.fields["image"].widget.attrs["class"] += " w-100 w-sm-50"