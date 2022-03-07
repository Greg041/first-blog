from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Post(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateField()
    excerpt = models.TextField(max_length=500)
    content = models.TextField()
    image = models.ImageField(upload_to="images")
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    category = models.ManyToManyField(Category)
    slug = models.CharField(max_length=100, default="", db_index=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("single_post_view", kwargs={"slug": self.slug})
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    comment = models.TextField(max_length=1000)

    def __str__(self):
        return self.username


