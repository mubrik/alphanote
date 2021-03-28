from django import forms
from notebooks.models import NoteBook


class CreateNoteBookForm(forms.ModelForm):
    
    class Meta:
        model = NoteBook
        fields = ['name', ]