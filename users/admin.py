# Django imports
from django.contrib import admin
# Local imports
## Models
from users.models import User


admin.site.register(User)