from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel 
from django_extensions.db.fields import RandomCharField 
from .managers import NoteBookManager

# get the default user for the project/app
UserModel = get_user_model()


class NoteBook(TimeStampedModel):
    ''' subclass of time stamped model, includes a created and modified field 
    '''
    # fields
    # uses randomchar from extensions to generate unique chars
    id = RandomCharField(length=12, unique=True, primary_key=True) 
    name = models.CharField(max_length=70, blank=False,)
    created_by = models.ForeignKey(UserModel, blank=True, null=False, on_delete=models.CASCADE, related_name='created_notebooks')

    # custom Manager
    objects = NoteBookManager()

    def __str__(self):
        return f'notebook: {self.name}'

    @property
    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('notebook_detail', args=[str(self.id)])

    def note_urls(self):
        return [note.get_absolute_url for note in self.notebook_notes.all()]

    def note_list(self):
        return [note.title for note in self.notebook_notes.all()]

    def notes_query(self):
        return self.notebook_notes.all()