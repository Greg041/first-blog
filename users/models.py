# Django imports
from django.db import models
from django.contrib.auth.models import AbstractUser
# Third party imports
import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    email = models.EmailField('Email', unique=False, blank=False, null=True)
    
    
    def __str__(self):
        return f'{self.get_full_name()} ({self.email}) - {self.id}'