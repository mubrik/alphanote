from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django_extensions.db.models import TimeStampedModel 
from django_extensions.db.fields import RandomCharField 
from .managers import NoteManager
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField

# get the default user for the project/app
UserModel = get_user_model()

def title_default():
    """ creates a default title for notes, implement further """
    return "Untitled Note"

class Note(TimeStampedModel):
    ''' subclass of time stamped model, includes a created and modified field 
        authstamped created_by is subbed out
    '''
    # fields
    # uses randomchar from extensions to generate unique chars 
    id = RandomCharField(length=12, unique=True, primary_key=True) 
    title = models.CharField(max_length=50, blank=True, default=title_default)
    content = SummernoteTextField(blank=True)
    notebook = models.ManyToManyField('notebooks.NoteBook', related_name='notebook_notes', blank=True)
    created_by = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=False, blank=True, related_name='created_notes')

    # custom Manager
    objects = NoteManager()

    def __str__(self):
        return f'note title: {self.title}'

    @property
    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse('note_detail', args=[str(self.id)])

