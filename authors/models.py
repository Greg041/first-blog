from django.db import models
from django.conf import settings
# Third party imports
from django_countries.fields import CountryField
from cloudinary.models import CloudinaryField
import uuid

# Create your models here.
class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False)
    biography = models.TextField("Biografía", null=True, blank=True)
    picture = CloudinaryField("Author image")
    country = CountryField("País", blank_label="Seleccione el país")
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.email})"