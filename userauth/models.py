from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.models import TimeStampedModel
from django_extensions.db.fields import RandomCharField 


class User(TimeStampedModel, AbstractUser):
    ''' Base user model,
        Extends django base abstract user and a timestamped model (created, modified),
        id and pk is randomcharfield, 10 keys
    '''
    
    id = RandomCharField(length=10, unique=True, primary_key=True ) 
    username = models.CharField(max_length=30, blank=False, null=False, unique=True,)