from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
import os

UserModel = get_user_model()

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        if not UserModel.objects.filter(username="notedadmin").exists():
            UserModel.objects.create_superuser("notedadmin", "mubrikdev@gmail.com", os.environ['adminkey'])
            self.stdout.write('Successfully created admin user')