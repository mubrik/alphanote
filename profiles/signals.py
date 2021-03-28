from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BaseProfile
from allauth.account.signals import user_signed_up

# get the default user for the project/app
UserModel = get_user_model()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print('creating profile')
        BaseProfile.objects.create(user=instance)
        print(f'profile created for {instance.username}')
