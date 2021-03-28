from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel
from .managers import ProfileManager

# get the default user for the project/app
UserModel = get_user_model()


def user_profile_picture_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    # uploaded_date = datetime.datetime.now()
    # year, month, day = (uploaded_date.strftime('%Y'), uploaded_date.strftime('%B'), uploaded_date.strftime("%d"))
    return f'users/{instance.user.username}/profile-picture/{filename}'



class BaseProfile(TimeStampedModel, models.Model):
    """
    Base profile model, can be extended to other models,
    Signals is used to create profile,
    extends timestamped to get created and modified dates,
    """
    user = models.OneToOneField(UserModel,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                related_name='user_profile')
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        default='default.png', upload_to=user_profile_picture_path, blank=True, )

    # custom manager
    objects = ProfileManager()

    # Metadata
    class Meta:
        ordering = ['user', 'created']

    # Methods
    def __str__(self):
        return f'{self.user.username} profile'

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('profile_detail')
