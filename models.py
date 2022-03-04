from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateField()
    excerpt = models.TextField(max_length=500)
    content = models.TextField()
    image = models.ImageField(upload_to="images")
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


