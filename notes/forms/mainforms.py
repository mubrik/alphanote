from django import forms
from django.contrib.auth import get_user_model
from django_summernote.widgets import SummernoteInplaceWidget
from notes.models import Note

# get the default user for the project/app
UserModel = get_user_model()

class CustomCheckbox (forms.CheckboxSelectMultiple):

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option['label'] = value.instance.name
        return option
    
    def id_for_label(self, *args, **kwargs):
        test = super(CustomCheckbox, self).id_for_label(*args, **kwargs)
        return test

class CreateNoteForm(forms.ModelForm):
    ''' creates a new note
        filters by usermodel to get notebook queryset 
    '''

    class Meta:
        model = Note
        widgets = {
            'notebook': CustomCheckbox,
        }
        fields = ['title', 'content', 'notebook', ]

    def __init__(self, user=None, *args, **kwargs):
        super(CreateNoteForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget = SummernoteInplaceWidget(attrs={'summernote': {'width': '100%', }})
        if user:
            self.fields['notebook'].queryset = UserModel.objects.get(username=user.username).created_notebooks.all()
            self.fields['notebook'].label = 'Notebooks:'


class CustomNotebookForm(CreateNoteForm):

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.auto_id = 'id_for_%s'
        del self.fields['content']
    