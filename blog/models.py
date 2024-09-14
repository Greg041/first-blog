from django.db import models
from django.utils.text import slugify
from django.urls import reverse
# Third party apps imports
from cloudinary.models import CloudinaryField
from tinymce.models import HTMLField
from uuid import uuid4


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    excerpt = HTMLField(max_length=500)
    content = HTMLField()
    image = CloudinaryField("image")
    author = models.ForeignKey("authors.Author", on_delete=models.CASCADE, null=False)
    category = models.ManyToManyField(Category)
    slug = models.CharField(max_length=100, default="", db_index=True, unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("single_post", kwargs={"id":self.id})
    

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    comment = models.TextField(max_length=1000)

    def __str__(self):
        return self.username