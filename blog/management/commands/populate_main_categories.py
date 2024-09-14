from django.core.management.base import BaseCommand
from blog.models import Category


class Command(BaseCommand):
    help = "Creates the main blog posts categories in DDBB"

    def handle(self, *args, **kwargs):
        main_categories = [
            "Animé",
            "Videojuegos",
            "Tecnología",
            "Gadgets",
            "Diseño"
        ]
        self.stdout.write(
            self.style.MIGRATE_LABEL("Populating Category table with main categories")
        )
        for category in main_categories:
            Category.objects.get_or_create(name=category)
        self.stdout.write(
            self.style.SUCCESS("The main post categories were successfully populated in DDBB")
        )